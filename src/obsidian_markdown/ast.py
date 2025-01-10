import re
from typing import Any, Iterable, Union
from dataclasses import dataclass


@dataclass
class ASTnode:
    name: str
    pattern: re.Pattern | None = None
    raw: str = ""  # store the raw text
    # NOTE: do not use mutable default value for children
    children: list["ASTnode"] = None
    parent: Union["ASTnode", None] = None
    data: dict[str, Any] = None  # store the meta fields
    is_leaf: bool = False

    def __post_init__(self):
        self.children = self.children or []
        self.data = self.data or {}

    def __repr__(self) -> str:
        return f"<ASTNode: {self.name}>"

    def filter(self, name: str) -> Iterable["ASTnode"]:
        for child in self.children:
            if child.name == name:
                yield child
            else:
                yield from child.filter(name)

    def print(self, indent: int = 0):
        print(
            f"{indent *' '}{self.name}: {str(self.data)[:20]} | {repr(self.raw)[:20]}"
        )
        if len(self.children) > 0:
            for child in self.children:
                child.print(indent + 2)
