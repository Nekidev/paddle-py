from pathlib import Path

import re
import sys

from datamodel_code_generator import generate, DataModelType, InputFileType

from black import format_file_in_place, WriteBack, Mode


sys.setrecursionlimit(5000)

print("Generating models...")

generate(
    input_=Path("openapi.yml"),
    input_file_type=InputFileType.OpenAPI,
    input_filename="openapi.yml",
    output=Path("./paddle/schemas"),
    output_model_type=DataModelType.PydanticV2BaseModel,
)


import ast
import astor
from pathlib import Path


def field_ast(type: str, args, keywords):
    return ast.Subscript(
        value=ast.Name(id="Annotated", ctx=ast.Load()),
        slice=ast.Tuple(
            elts=[
                ast.Name(id=type, ctx=ast.Load()),
                ast.Call(
                    func=ast.Name(id="Field", ctx=ast.Load()),
                    args=args,
                    keywords=keywords,
                ),
            ],
            ctx=ast.Load(),
        ),
        ctx=ast.Load(),
    )


def transform_node(node):
    import ast

    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
        if node.func.id == "confloat":
            return field_ast("float", node.args, node.keywords)
        elif node.func.id == "constr":
            return field_ast("str", node.args, node.keywords)
        elif node.func.id == "conint":
            return field_ast("int", node.args, node.keywords)

    return node


def transform_file(file_path: Path):
    source = file_path.read_text()
    tree = ast.parse(source)

    class Transformer(ast.NodeTransformer):
        def visit_Call(self, node):
            new_node = transform_node(node)
            if new_node is not node:
                return ast.copy_location(new_node, node)
            return self.generic_visit(node)

    tree = Transformer().visit(tree)
    tree = ast.fix_missing_locations(tree)

    new_code = astor.to_source(tree)

    new_code = "from typing import Annotated; from pydantic import Field\n" + new_code

    new_code = re.sub(r"\(([a-zA-Z0-9_]+: )", r"\1 (", new_code)
    new_code = new_code.replace("constr,", "")
    new_code = new_code.replace("conint,", "")
    new_code = new_code.replace("confloat,", "")

    lines = new_code.splitlines()

    for i, line in enumerate(lines):
        if line.startswith("from __future__"):
            # move line to the top, __future__ imports must be first

            lines.insert(0, lines.pop(i))
            break

    new_code = "\n".join(lines)

    file_path.write_text(new_code)


for file in Path("./paddle/schemas").rglob("*.py"):
    print(f"Formatting {file}...")

    transform_file(file)
    format_file_in_place(
        file,
        fast=True,
        mode=Mode(),
        write_back=WriteBack.YES,
    )

print("Done.")
