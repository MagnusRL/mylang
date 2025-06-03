import ast
import operator as op
import math
from parser import parse_expression

# Supported operators
OPS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow
}

def eval_node(node, variables):
    if isinstance(node, ast.Expression):
        return eval_node(node.body, variables)
    elif isinstance(node, ast.BinOp):
        left = eval_node(node.left, variables)
        right = eval_node(node.right, variables)
        return OPS[type(node.op)](left, right)
    elif isinstance(node, ast.Num):
        return node.n
    elif isinstance(node, ast.Name):  # Variable like 'a'
        if node.id in variables:
            return variables[node.id]
        else:
            raise NameError(f"Undefined variable: {node.id}")
    else:
        raise TypeError(f"Unsupported type: {type(node)}")


def evaluate(expr_ast, variables=None):
    return eval_node(expr_ast, variables or {})

FUNCTIONS = {}

def define_function(name, param, body_expr):
    FUNCTIONS[name] = (param, body_expr)

def call_function(name, value):
    param, body = FUNCTIONS[name]
    # Replace param with value and evaluate
    expr = body.replace(param, str(value))
    expr_ast = parse_expression(expr)
    return evaluate(expr_ast)
