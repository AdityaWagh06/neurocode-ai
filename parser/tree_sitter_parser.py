
from pathlib import Path

import tree_sitter_python as tspython
from tree_sitter import Language, Parser


PYTHON_LANGUAGE = Language(tspython.language())
PYTHON_PARSER = Parser(PYTHON_LANGUAGE)


def parse_with_tree_sitter(file_path: Path) -> dict:
    source_code = file_path.read_bytes()
    tree = PYTHON_PARSER.parse(source_code)

    functions = []
    classes = []

    def visit(node):
        if node.type in {"function_definition"}:
            name_node = node.child_by_field_name("name")

            if name_node:
                functions.append({
                    "name": source_code[
                        name_node.start_byte:name_node.end_byte
                    ].decode("utf-8"),
                    "start_line": node.start_point.row + 1,
                    "end_line": node.end_point.row + 1,
                })

        elif node.type == "class_definition":
            name_node = node.child_by_field_name("name")

            if name_node:
                classes.append({
                    "name": source_code[
                        name_node.start_byte:name_node.end_byte
                    ].decode("utf-8"),
                    "start_line": node.start_point.row + 1,
                    "end_line": node.end_point.row + 1,
                })

        for child in node.children:
            visit(child)

    visit(tree.root_node)

    return {
        "file": str(file_path),
        "functions": functions,
        "classes": classes,
        "has_syntax_errors": tree.root_node.has_error,
    }
