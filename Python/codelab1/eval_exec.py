# eval_exec.py
def calc(expr: str):
    x = 10
    y = 5
    return eval(expr)  

def run_dynamic():
    code = "print('from exec')"
    exec(code)         

def safe():
    return "no issues here"
