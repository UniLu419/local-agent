import ast
import operator

from langchain_core.tools import tool

# Whitelist of safe AST node types → Python operators
_OPERATORS: dict = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.FloorDiv: operator.floordiv,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def _safe_eval(node: ast.expr) -> float | int:
    """Recursively evaluate a safe arithmetic AST node."""
    if isinstance(node, ast.Constant):
        if not isinstance(node.value, (int, float)):
            raise ValueError(f"Unsupported constant type: {type(node.value)}")
        return node.value
    if isinstance(node, ast.BinOp):
        op_fn = _OPERATORS.get(type(node.op))
        if op_fn is None:
            raise ValueError(f"Unsupported operator: {type(node.op).__name__}")
        return op_fn(_safe_eval(node.left), _safe_eval(node.right))
    if isinstance(node, ast.UnaryOp):
        op_fn = _OPERATORS.get(type(node.op))
        if op_fn is None:
            raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")
        return op_fn(_safe_eval(node.operand))
    raise ValueError(f"Unsupported expression node: {type(node).__name__}")


@tool
def calculator(expression: str) -> str:
    """Safely evaluate a mathematical expression.

    Supports: +, -, *, /, ** (power), % (modulo), // (floor division).
    Does NOT support functions, variables, or arbitrary code.

    Args:
        expression: A math expression string, e.g. "2 ** 10 + 3 * 4"

    Returns:
        The numeric result as a string, or an error message.
    """
    try:
        tree = ast.parse(expression.strip(), mode="eval")
        result = _safe_eval(tree.body)
        # Return int if result is a whole number
        if isinstance(result, float) and result.is_integer():
            return str(int(result))
        return str(result)
    except Exception as exc:
        return f"Error: {exc}"
