#---------------------------------------------------------------------------
# 작성자: 3002 기동주
# 작성 목적: [파이썬 1일차 실습 - 리스트 + 딕셔너리 기반 데이터 필터링기]
# 작성일: 2026.01.22
#
# 변경사항 내역(날짜, 변경목적, 변경내용 순으로 기입)
#---------------------------------------------------------------------------


# 다음은 직원(Employee)들의 정보를 담은 리스트입니다.
# 이 데이터를 활용하여 아래 조건을 만족하는 필터링 로직을 작성하세요.
employees = [
  {"name": "Alice", "department": "Engineering", "age": 30, "salary": 85000},
  {"name": "Bob", "department": "Marketing", "age": 25, "salary": 60000},
  {"name": "Charlie", "department": "Engineering", "age": 35, "salary": 95000},
  {"name": "David", "department": "HR", "age": 45, "salary": 70000},
  {"name": "Eve", "department": "Engineering", "age": 28, "salary": 78000},
]


# 1) 부서가 "Engineering"이고 salary >= 80000인 직원들의 이름만 리스트로 출력하세요.

result1 = [i["name"] for i in employees 
           if i["department"] == "Engineering" and i["salary"] >= 80000]    
print("1) ", result1)


# 2) 30세 이상인 직원의 이름과 부서를 튜플 (name, department) 형태로 리스트로 출력하세요.

result2 = [(i["name"], i["department"]) 
           for i in employees if i["age"] >= 30]
print("2) ", result2)


# 3) 급여 기준으로 직원 리스트를 salary 내림차순으로 정렬하고, 상위 3명의 이름과 급여를 출력하세요.
from operator import itemgetter

desc = sorted(employees, key=itemgetter("salary"), reverse=True)

result3 = [(i["name"], i['salary']) for i in desc[:3]]
print("3) ", result3)


# 4) 모든 부서별 평균 급여를 출력하는 코드를 작성해보세요

from collections import defaultdict

salary = defaultdict(int) # int() == 0
count = defaultdict(int)

for i in employees:
    dept = i["department"]
    salary[dept] += i["salary"]
    count[dept] += 1

avg_salary = {dept: salary[dept] / count[dept] for dept in salary}

print("4) ", avg_salary)
