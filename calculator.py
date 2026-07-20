from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path
import math
import ast
import operator

app = FastAPI(title="Calculator API")

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


class CalcRequest(BaseModel):
    expression: str


class CalcResponse(BaseModel):
    expression: str
    result: str


ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def safe_eval(expression: str) -> float:
    expression = expression.replace("^", "**")
    expression = expression.replace("×", "*")
    expression = expression.replace("÷", "/")

    tree = ast.parse(expression, mode="eval")

    def _eval(node):
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return float(node.value)
        if isinstance(node, ast.BinOp) and type(node.op) in ALLOWED_OPERATORS:
            left = _eval(node.left)
            right = _eval(node.right)
            return ALLOWED_OPERATORS[type(node.op)](left, right)
        if isinstance(node, ast.UnaryOp) and type(node.op) in ALLOWED_OPERATORS:
            operand = _eval(node.operand)
            return ALLOWED_OPERATORS[type(node.op)](operand)
        raise ValueError("Unsupported expression")

    result = _eval(tree.body)
    if not math.isfinite(result):
        raise ValueError("Result is not finite")
    return result


@app.get("/")
def read_index():
    return FileResponse(STATIC_DIR / "index.html")


@app.post("/api/calc", response_model=CalcResponse)
def calculate(payload: CalcRequest):
    expression = payload.expression.strip()
    if not expression:
        raise HTTPException(status_code=400, detail="Expression is required")

    try:
        result = safe_eval(expression)
    except (SyntaxError, ValueError, ZeroDivisionError, OverflowError):
        raise HTTPException(status_code=400, detail="Invalid expression") from None

    formatted_result = format(result, ".12g")
    return CalcResponse(expression=expression, result=formatted_result)
