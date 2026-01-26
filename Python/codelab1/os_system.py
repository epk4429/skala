# os_system.py
import os

def run_cmd():
    os.system("from os")
# 중첩 호출 확인용
def nested():
    print(os.system("print + os nested test")) 
