#---------------------------------------------------------------------------
# 작성자: 3002 기동주
# 작성 목적: [파이썬 1일차 - Codelab ①]: 코드 실행 전 취약점 찾기
# 작성일: 2026.01.23
#
# 변경사항 내역(날짜, 변경목적, 변경내용 순으로 기입)
#---------------------------------------------------------------------------
#
# • 가이드
#  ‣    ast.NodeVisitor를 상속받아 코드 내의 모든 함수 호출(Call) 노드를 탐색
#  ‣    위험 함수(eval, exec, pickle.load)와 함께, 실무에서 금지하는 os.system 등을 감지
#  ‣    단순 탐지를 넘어, 어떤 파일의 몇 번째 줄에서 위반이 발생했는지 리포트를 생성
# • 라이브러리
#  ‣    import ast
#
#----------------------------------------------------------------------------
# 
# 검사기 사용법: python codelab1.py --file '검사할 파일 경로'
#              python codelab1.py --dir '검사할 디렉토리 경로'
#-----------------------------------------------------------------------------
import ast
import argparse
from pathlib import Path
from dataclasses import dataclass
from collections import defaultdict

@dataclass
class Violation:
    file: str
    line: int
    call: str
    source_line: str


# -------------------함수 이름 정규화--------------------------------------
# eval("x") → "eval" 처럼 함수 호출 대상이 무엇인지를 문자열로 정규화 하는 함수
def normalize_call_name(func_node) -> str | None:
    # eval이나 exec 같이 대상이 name인 경우 그대로 return
    if isinstance(func_node, ast.Name):
        return func_node.id

    # 호출 대상이 a.b 처럼 속성을 호출하는 형태일 경우
    if isinstance(func_node, ast.Attribute):
        # func_node.attr: 맨 마지막 속성 담기 a.b.c면 "c"
        parts = [func_node.attr] 
        # func_node.value: a.b.c라면 value는 a.b
        value = func_node.value

        # 만약 계속해서 attribute로 이어진다면 a.b.c.d를 ["a","b","c","d"] 형태로
        while isinstance(value, ast.Attribute):
            parts.append(value.attr)
            value = value.value

        # 이제 가장 왼쪽이 name이면 마지막으로 part에 추가, name이 아니면 정규화 불가로 None 반환
        if isinstance(value, ast.Name):
            parts.append(value.id)
        else:
            return None

        # 지금까지 a.b.c를 뒤에서 부터 접근했기 때문에 정상 순서로 revrse
        parts.reverse()
        # "." 으로 이어 문자열로 반환
        return ".".join(parts)
    # 호출 대상이 name, attribute 둘 다 아닌 경우 None
    return None
# ----------------------------------------------------------------------

# -------Visitor 클래스--------------------------------------------------

class CallVisitor(ast.NodeVisitor):                     # banned가 많은 경우 set으로 체크하는 속도가 빠름
    def __init__(self, filename: str, lines: list[str], banned: set[str]):
        self.filename = filename
        self.lines = lines
        self.banned = banned
        # Violation 객체만 들어가도록
        self.violations: list[Violation] = []

    def visit_Call(self, node: ast.Call):
        # 호출명을 문자열로 정규화
        call_name = normalize_call_name(node.func)

        # banned 와 비교
        if call_name in self.banned:
            # 만약 Node line number가 없으면 None으로 처리
            lineno = getattr(node, "lineno", None)

            # line number가 있으면 원문 한 줄을 확보
            # 리포트 내용이 없어도 항상 문자열이 되도록 빈 문자열 생성
            source_line = ""
            if lineno is not None and 1 <= lineno <= len(self.lines):
                source_line = self.lines[lineno - 1].strip()

            # 리포트에 기록
            self.violations.append(
                Violation(
                    file=self.filename,
                    line=lineno if lineno is not None else -1,
                    call=call_name,
                    source_line=source_line,
                )
            )
        # 중첩 호출까지 탐색
        self.generic_visit(node)
# ----------------------------------------------------------------------


# ------------ 파일 검사 ------------------------------------------------
                                                # 위반 사항을 리스트로 반환
def scan_file(path: Path, banned: set[str]) -> list[Violation]:
    try:
        code = path.read_text(encoding="utf-8")
    except Exception as e:
        # 파일 읽기 실패하면 출력
        print(f"[Error] Failed to read: {path} ({e})")
        return []

    # AST 파싱
    try:
        tree = ast.parse(code)
    # syntaxerror 발생 시 위치 출력    
    except SyntaxError as e:
        print(f"[Error] SyntaxError in {path} (line {e.lineno})")
        return []

    # 원문을 lines[lineno-1]로 만들기 위해 splilines
    lines = code.splitlines()
    # 탐지기 인스턴스 생성 및 트리 방문
    visitor = CallVisitor(filename=str(path), lines=lines, banned=banned)
    visitor.visit(tree)
    return visitor.violations
#------------------------------------------------------------------------

#------------------- 경로 안 파일 collect 함수 ----------------------------

def collect_files(target: Path) -> list[Path]:
    if target.is_file():
        return [target] if target.suffix == ".py" else []
    # 경로가 폴더면 재귀적으로 .py 파일 모두 탐색
    if target.is_dir():
        return list(target.rglob("*.py"))
    return []
#------------------------------------------------------------------------

#------------------- main 함수 -------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="AST 기반 자동 보안 검사기")
    # 파일이나이나 디렉토리 동시에 X
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--file", type=str, help="검사할 .py 파일 경로")
    group.add_argument("--dir", type=str, help="검사할 디렉토리 경로(하위 .py 모두 검사)")
    args = parser.parse_args()
    
    target = Path(args.file if args.file else args.dir)

    # 잘못된 경로 입력 시 종료
    if not target.exists():
        raise SystemExit(f"[Error] 경로가 존재하지 않습니다: {target}")

    # 위험 함수 목록
    banned = {"eval", "exec", "pickle.load", "os.system"}

    # 검사할 파일 불러오기
    py_files = collect_files(target)
    if not py_files:
        raise SystemExit("[Error] 검사할 파일이 없습니다.")

    # 위험 함수를 저장할 리스트 초기화 후 extend로 일반 리스트에 저장
    all_violations: list[Violation] = []
    for i in py_files:
        all_violations.extend(scan_file(i, banned=banned))

    # 리포트 시작
    grouped = defaultdict(list)
    for v in all_violations:
        grouped[v.file].append(v)

    print("=" * 80)
    print("[REPORT] AST 보안 검사 결과")
    print("=" * 80)

    if not all_violations:
        print("검출된 위험 함수가 없습니다.")
    else:
        total = 0
        for file_path in sorted(grouped.keys()):
            print(f"\n[{Path(file_path).name}]")  
            for idx, v in enumerate(sorted(grouped[file_path], key=lambda x: x.line), start=1):
                total += 1
                print(f"  ({idx}) line {v.line:<4} {v.call}")
                if v.source_line:
                    print(f"      > {v.source_line}")
        print(f"\n총 위반: {total}건")

    print("=" * 80)


if __name__ == "__main__":
    main()