#---------------------------------------------------------------------------
# 작성자: 3002 기동주
# 작성 목적: [파이썬 2일차 실습 - OOP 기반 AI 추천 주문 시스템 설계]
#           객체지향 프로그래밍(OOP) 개념 (클래스, 상속, @property 등)을 활용해
#           AI 추천 기능을 포함한 주문 시스템을 설계하고 구현
# 작성일: 2026.01.26
#
# 변경사항 내역(날짜, 변경목적, 변경내용 순으로 기입)
#---------------------------------------------------------------------------
#
# 한 스타트업이 온라인 음료 주문 플랫폼을 개발 중이다.
# • 사용자의 주문 이력을 기반으로 머신러닝 없이도 간단한 추천 시스템을 포함하려 한다.
# • 이 시스템은 다음 기능을 포함해야 한다.
#   ‣ 다양한 음료 메뉴 정의
#     (이름, 가격, 태그: 예: '커피', '차', '콜드', '뜨거운')
#   ‣ 사용자의 주문 내역 저장 (사용자는 임의로 설정 후 진행)
#   ‣ 최근 주문된 음료를 바탕으로 유사한 태그의 음료 추천
#   ‣ 총 주문 금액 계산 (총합, 평균 등 포함)
#---------------------------------------------------------------------------
from dataclasses import dataclass
from datetime import datetime
from typing import List, Set

@dataclass(frozen=True) 
class Menu:
    name: str
    price: int
    tags: List[str] 

    def tag_score(self, base_tag: Set[str]) -> int:
        return len(set(self.tags) & base_tag) # 집합으로 안들어오면 & 연산이 불가능해서 집합으로 만들기

# Hot, Cold 음료 분류해서 상속
@dataclass(frozen=True)
class HotBeverage(Menu):

    @property
    def temp(self) -> str:
        return "HOT"
    
@dataclass(frozen=True)
class ColdBeverage(Menu):

    @property
    def temp(self) -> str:
        return "COLD"

# 주문 시 총 주문 금액 계산과 전체 태그를 속성으로
@dataclass
class Order:
    items: List[Menu]
    created_at: datetime

    @property
    def total(self) -> int:
        return sum(i.price for i in self.items)

    @property
    def avg(self) -> float:
        return self.total / len(self.items) if self.items else 0.0

    @property
    def tags(self) -> Set[str]:
        t: Set[str] = set()
        for i in self.items:
            t.update(i.tags)
        return t

# 사용자의 주문 내역 저장
class User:
    def __init__(self, name: str):
        self.name = name
        self.orders: List[Order] = []

    def order(self, items: List[Menu]) -> Order:
        o = Order(items=items, created_at=datetime.now())
        self.orders.append(o)
        return o

    @property
    def total_spent(self) -> int:
        return sum(o.total for o in self.orders)

    @property
    def avg_spent(self) -> float:
        return self.total_spent / len(self.orders) if self.orders else 0.0

    @property
    def recent_order(self) -> Order | None:
        return self.orders[-1] if self.orders else None

# 최근 주문 기반 음료 추천 함수
def recommendation(user: User, menu: List[Menu], k: int = 2) -> List[Menu]:
    if not user.recent_order:
        print("주문 이력이 없어 추천이 어렵습니다.")
        return []

    recent_names = {i.name for i in user.recent_order.items}
    base_tags = user.recent_order.tags
    

    recommend = []
    for m in menu:
        if m.name in recent_names: # 직전 주문 음료는 추천에서 제외
            continue
        score = m.tag_score(base_tags)
        if score > 0:
            recommend.append((score, m.price, m.name, m))

    recommend.sort(key=lambda x: (-x[0], x[1])) # 추천 기준 1순위는 겹치는 태그, 2순위는 낮은 가격순
    return [c[-1] for c in recommend[:k]]


# 메인 실행 함수
if __name__ == "__main__":
    
    menu = [
        HotBeverage("아메리카노", 3500, ["커피", "뜨거운"]),
        HotBeverage("카페라떼", 3500, ["커피", "밀크", "뜨거운"]),
        HotBeverage("녹차", 4000, ["차", "뜨거운"]),
        HotBeverage("라떼", 4500, ["커피", "뜨거운", "우유"]),
        ColdBeverage("아이스 아메리카노", 3800, ["커피", "콜드"]),
        ColdBeverage("아이스 라떼", 4800, ["커피", "콜드", "우유"]),
        ColdBeverage("아이스티", 4200, ["차", "콜드"]),
        ColdBeverage("레몬에이드", 4300, ["에이드", "콜드"]),
        ColdBeverage("수박에이드", 4600, ["에이드", "콜드"])
    ]

    user = User("DJKEE")
    print(f"사용자: {user.name}")
    print("입력 예시: 1 또는 1,4 또는 q(종료)")

    while True:
        print("\n[메뉴]")
        for idx, m in enumerate(menu, start=1):
            print(f"{idx}. {m.name}({m.temp}) {m.price}원 / {m.tags}")

        raw = input("\n주문할 메뉴 번호(ex. 1 또는 1,4) 또는 q: ").strip().lower()
        if raw == "q":
            print("\n종료합니다.")
            break

        
        idxs = [int(x.strip()) for x in raw.split(",") if x.strip()]
        items = [menu[i - 1] for i in idxs]
        
        o = user.order(items)
        print(f"\n[주문 완료] 총액={o.total}원, 평균={o.avg:.0f}원")

        print("\n[AI 추천] (최근 주문 태그 기반 추천)")
        recd = recommendation(user, menu, k=2)
        if not recd:
            print("- 추천할 메뉴가 없습니다.")
        else:
            for b in recd:
                overlap = set(b.tags) & user.recent_order.tags
                print(f"- {b.name}({b.temp}) {b.price}원 | 매칭태그={sorted(overlap)} | 'AI 점수'={len(overlap)}")

        print("\n[정산]")
        print(f"- 총 주문 횟수: {len(user.orders)}")
        print(f"- 총 주문 금액: {user.total_spent}원")
        print(f"- 주문 평균 금액: {user.avg_spent:.0f}원")
        print("=" * 80)