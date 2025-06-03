import ast

def parse_expression(expr: str):
    try:
        tree = ast.parse(expr, mode='eval')
        return tree
    except SyntaxError as e:
        raise SyntaxError(f"Invalid expression: {expr}. Error: {e.msg}")
