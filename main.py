from typing import Any

from obsidian_markdown.obsidian_markdown import ObsidianMarkdown
from obsidian_markdown.block_parser import ListBlockParser


def print_ast(ast: list[dict[str, Any]], indent: int = 0):
    for node in ast:
        if "children" in node:
            print_ast(node["children"], indent + 2)
            continue
        print(f"{indent * ' '}{node['type']}: {node.get("raw", "")}")


def main():
    # example_markdowns = [
    #     # "C:/Users/admin/OneDrive/obsidian/专题学习/狄里克雷混合模型.md",
    #     "C:/Users/admin/OneDrive/obsidian/计算机/windows终端配置.md",
    # ]
    # for fn in example_markdowns:
    #     print(fn)
    #     with open(fn, "r", encoding="utf-8") as f:
    #         content = f.read()
    #
    #     ast = ObsidianMarkdown().parse(content)
    #     ast.print()
    #     for node in ast.filter("callout"):
    #         print(node.raw)
    #         print(node.data)
    #         print(node.children[0].raw)

    text = "* AAA\n" "* BBB\n" "* CCC\n"
    forward, node, backward = ListBlockParser()(text)
    print(node)
    print(node.children)
    node.print()
    # print(forward)
    # print(node)
    # print(backward)


if __name__ == "__main__":
    main()
