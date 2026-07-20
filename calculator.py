from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
import math
import ast
import operator
import os

app = FastAPI(title="Calculator API")

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# CORS: allow origins configured via ALLOW_ORIGINS env var (comma-separated). Default to same-origin only.
allow_origins = os.getenv("ALLOW_ORIGINS")
if allow_origins:
    origins = [o.strip() for o in allow_origins.split(",") if o.strip()]
else:
    origins = []

if origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


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

    # Safety limits
    MAX_EXPONENT = 100
    MAX_RESULT_ABS = 1e12

    def _eval(node):
        # Numbers (ast.Constant for py3.8+, ast.Num for older ASTs)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return float(node.value)
        if isinstance(node, ast.Num):
            return float(node.n)

        # Binary operations
        if isinstance(node, ast.BinOp) and type(node.op) in ALLOWED_OPERATORS:
            left = _eval(node.left)
            right = _eval(node.right)

            # Mitigate huge exponents (DoS)
            if isinstance(node.op, ast.Pow) or type(node.op) is ast.Pow:
                if abs(right) > MAX_EXPONENT:
                    raise ValueError("Exponent too large")

            result = ALLOWED_OPERATORS[type(node.op)](left, right)

            if not math.isfinite(result) or abs(result) > MAX_RESULT_ABS:
                raise ValueError("Result is not finite or exceeds allowed magnitude")

            return result

        # Unary ops
        if isinstance(node, ast.UnaryOp) and type(node.op) in ALLOWED_OPERATORS:
            operand = _eval(node.operand)
            result = ALLOWED_OPERATORS[type(node.op)](operand)
            if not math.isfinite(result) or abs(result) > MAX_RESULT_ABS:
                raise ValueError("Result is not finite or exceeds allowed magnitude")
            return result

        # Unsupported nodes
        raise ValueError(f"Unsupported expression node: {type(node).__name__}")

    # Only allow an Expression AST at top-level
    if not isinstance(tree, ast.Expression):
        raise ValueError("Invalid expression")

    result = _eval(tree.body)
    return result


@app.get("/")
def read_index():
    index_file = STATIC_DIR / "index.html"
    if not index_file.exists():
        # Return a friendly JSON response explaining missing assets
        raise HTTPException(status_code=404, detail="Static UI not found. Ensure static/index.html is present.")
    return FileResponse(index_file)


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
