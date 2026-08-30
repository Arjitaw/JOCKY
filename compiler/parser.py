import json
from lark import Lark
from pathlib import Path
from .Transformer import JockyTransformer

BASE_DIR = Path(__file__).resolve().parent
with open(BASE_DIR / "grammar.lark","r") as file:
    grammar=file.read()

parser=Lark(
    grammar,
    start="start"
)

def parse_command(command):
    tree = parser.parse(command)

    transformer = JockyTransformer()

    return transformer.transform(tree)

print(parse_command("SYSTEM INFO"))