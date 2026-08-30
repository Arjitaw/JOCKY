import json
from lark import Lark
from Transformer import JockyTransformer

with open("grammar.lark","r") as file:
    grammar=file.read()

parser=Lark(
    grammar,
    start="start"
)

command="""
SYSTEM INFO
LIST FILES .
ENCRYPT FILE hello.txt
HASH FILE hello.txt
SEARCH FILE hello.txt IN .
PROCESSES
"""

tree=parser.parse(command)

transformer=JockyTransformer()

result=transformer.transform(tree)

print("command:")
print(command)

print("\nStructured command:")
print(json.dumps(result, indent=4))