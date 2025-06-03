from parser import parse_expression
from evaluator import evaluate
import re
from evaluator import define_function, call_function

def run_repl():
    print("Welcome to MyLang!")
    VARIABLES = {}
    while True:
        try:
            line = input("> ")
            if line in ("exit", "quit"):
                break

            line = line.replace("^", "**")  # Replace ^ with ** for exponentiation
            line = re.sub(r'(?<=\d)([a-zA-Z])', r'*\1', line) 
            line = re.sub(r'([a-zA-Z])(?=[a-zA-Z])', r'\1*', line)

            if "=" in line and "(" in line and ")" in line:
                # Function definition
                match = re.match(r"(\w+)\((\w+)\)\s*=\s*(.+)", line)
                if match:
                    name, param, body = match.groups()
                    define_function(name, param, body)
                    print(f"Defined {name}({param})")
                    continue

            match = re.match(r"(\w+)\((\d+)\)", line)
            if match:
                name, value = match.groups()
                result = call_function(name, int(value))
                print(result)
                continue


# Variable assignment: a = 5
            if "=" in line and "(" not in line:
                var, expr = map(str.strip, line.split("=", 1))
                expr = re.sub(r'(?<=\d)([a-zA-Z])', r'*\1', expr)
                expr = re.sub(r'([a-zA-Z])(?=[a-zA-Z])', r'\1*', expr)
                expr = expr.replace("^", "**")
                expr_ast = parse_expression(expr)
                VARIABLES[var] = evaluate(expr_ast, VARIABLES)
                print(f"{var} = {VARIABLES[var]}")
                continue


            expr_ast = parse_expression(line)
            result = evaluate(expr_ast, VARIABLES)
            print(result)
        except Exception as e:
            print(f"Error: {e}")
