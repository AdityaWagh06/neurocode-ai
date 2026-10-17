
import ast
from pathlib import Path


def parse_python_file(file_path: Path) -> dict:
    source_code = file_path.read_text(encoding="utf-8")

    try:
        tree = ast.parse(source_code, filename=str(file_path))
    except SyntaxError as error:
        return {
            "file": str(file_path),
            "classes": [],
            "functions": [],
            "error": str(error),
        }

    classes = []
    functions = []

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            classes.append({
                "name": node.name,
                "line": node.lineno,
                "end_line": node.end_lineno,
            })

        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            functions.append({
                "name": node.name,
                "line": node.lineno,
                "end_line": node.end_lineno,
            })

    return {
        "file": str(file_path),
        "classes": classes,
        "functions": functions,
        "error": None,
    }
