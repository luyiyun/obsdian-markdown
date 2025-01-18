import re
from itertools import zip_longest
from abc import abstractmethod

import yaml

from .ast import ASTnode


def preprocess(text, end="\n") -> str:
    if end and not text.endswith("\n"):
        text += "\n"
    return text


class BlockParser:
    @abstractmethod
    def get_ast_node(self, match: re.Match) -> ASTnode:
        pass

    def __call__(self, text: str) -> tuple[str | None, ASTnode | None, str | None]:
        text = preprocess(text)
        match = self.pattern.search(text)
        if not match:
            return None, None, text

        forward = text[: match.start()] if match.start() > 0 else None
        backward = text[match.end() :] if match.end() < len(text) else None
        node = self.get_ast_node(match)
        return forward, node, backward


class FrontMatterParser(BlockParser):
    def __init__(self) -> None:
        self.pattern = re.compile(r"---(\n*?)(.*?)(\n*?)---\n", re.DOTALL)

    def get_ast_node(self, match: re.Match) -> ASTnode:
        raw = match.group(2)
        data = yaml.load(raw, Loader=yaml.FullLoader)
        return ASTnode(
            "front_matter", pattern=self.pattern, raw=raw, data=data, is_leaf=True
        )


class CodeBlockParser(BlockParser):
    def __init__(self) -> None:
        self.pattern = re.compile(
            r"(?m:^)"
            r"(?P<indent>\s*)"
            r"```(?P<lang>.*?)\n"
            r"(?P<code>(?s:.)*?)"
            r"(?m:^)(?P=indent)```\s*(?m:$)",
        )
        # self.code_id_pattern = re.compile(r"\(\[<@#\$code_id (\d)&\*\%\)\]>")
        # self.init()

    # def init(self):
    #     self.code_nodes = []
    #
    # def preprocess(self, text: str) -> str:
    #     parts = self.pattern.split(text)
    #     match = len(parts) > 1
    #     if not match:
    #         return text
    #     others = parts[::4]
    #     indents = parts[1::4]
    #     langs = parts[2::4]
    #     codes = parts[3::4]
    #
    #     code_ids = []
    #     for i, (lang, code) in enumerate(zip(langs, codes)):
    #         code_ids.append(f"([<@#$code_id {i}&*%)]>")
    #         code = "\n".join([line[len(indents[i]) :] for line in code.split("\n")])
    #         self.code_nodes.append(
    #             ASTnode(
    #                 "code_block",
    #                 pattern=self.pattern,
    #                 raw=code,
    #                 data={"lang": lang},
    #                 is_leaf=True,
    #             )
    #         )
    #
    #     text_clean = ""
    #     for other, code_id, indent in zip(others, code_ids, indents):
    #         text_clean += other + indent + code_id
    #     text_clean += parts[-1]
    #     return text_clean

    def get_ast_node(self, match: re.Match) -> ASTnode:
        return ASTnode(
            "code_block",
            pattern=self.pattern,
            raw=match.group("code"),
            data={"lang": match.group("lang")},
            is_leaf=True,
        )


class SectionParser(BlockParser):
    def __init__(self, level: int = 1):
        self.level = level
        # (?m:^)表示启用多行模式的^，此时其不表示文本的开始，而是每一行的开始
        # 启用多行模式另一种用法是使用flag re.M，此时整个pattern中的所有^$
        # 都表示每一行的开始和结束，而不是整个文本的开始和结束
        # 这里，我们匹配的对象可能直接到达文本末尾，因此需要使用$来匹配

        # 我们还要避免会匹配到注释
        self.pattern = re.compile(
            r"(?m:^)"  # match start of line
            r" {0,3}"  # match 0-3 spaces
            rf"{'#' * level}"  # match specific-level number sign
            r" "  # match one space after level sign
            r"(?P<title>.*)\n"  # match title, here dot cannot match \n, so we use greedy mode
            r"(?P<content>([^`]|(```(?s:.)*?```)|(`.*?`))*?)"  # match the all content under the title, and the code block tags (```) must be paired
            rf"((?=(?m:^) {{0,3}}{"#" * level} )|$)",  # match the title line of next section, use loookahead assertion
        )

    def get_ast_node(self, match: re.Match) -> ASTnode:
        title = match.group("title")
        raw = match.group("content")
        return ASTnode(
            f"section{self.level}",
            pattern=self.pattern,
            raw=raw,
            data={"title": title},
        )


class MathBlockParser(BlockParser):
    def __init__(self) -> None:
        self.pattern = re.compile(r"^\s*\$\$(.*?)\$\$\s*\n", re.DOTALL | re.M)

    def get_ast_node(self, match: re.Match) -> ASTnode:
        return ASTnode(
            "math_block",
            pattern=self.pattern,
            raw=match.group(1),
            is_leaf=True,
        )


class CalloutParser(BlockParser):
    def __init__(self) -> None:
        self.pattern = re.compile(
            r"(?m:^)\s*?>\s*"  # 匹配行首的>和空格
            r"\[\!(?P<category>.*?)\]"  # 匹配category, 如![note]
            r"(?P<collapse>[-+]?)"  # 匹配是否存在折叠符号
            r"(?P<title>.*?)"  # 匹配title
            r"\n(?P<content>(?s:.)*?)"  # 匹配content
            r"((?=(?m:^)\s*?[^>])|$)",
        )
        self.line_start_pattern = re.compile(r"^\s*?>\s*", re.M)

    def get_ast_node(self, match: re.Match) -> ASTnode:
        category = match.group("category").strip()
        collapase = match.group("collapse").strip()
        title = match.group("title").strip()
        raw = match.group("content")
        # 需要处理以下content，将每一行前面带有的>和空格去掉
        raw = self.line_start_pattern.sub(r"", raw).strip()
        return ASTnode(
            "callout",
            pattern=self.pattern,
            raw=raw,
            data={
                "category": category,
                "collapse": collapase,
                "title": title,
            },
        )


class ImageLinkParser(BlockParser):
    def __init__(self) -> None:
        self.pattern = re.compile(
            r"(\!\[\[(?P<wiki>.+?)\]\])|(\!\[(?P<title>.*?)]\((?P<link>.+?)\))"
        )

    def get_ast_node(self, match: re.Match) -> ASTnode:
        data = {}
        if match["wiki"]:
            split_res = match["wiki"].split("|")
            data["link"] = split_res.pop(0)
            for s in split_res:
                if s.isdigit():
                    data["width"] = int(s)
                elif s == "center":
                    data["position"] = s
                else:
                    data["title"] = s
            data["wiki"] = True
        else:
            data["link"] = match["link"]
            data["title"] = match["title"]
            data["wiki"] = False

        if data["link"].endswith(".excalidraw"):
            data["category"] = "excalidraw"
        else:
            data["category"] = "img"

        return ASTnode(
            "image_link",
            pattern=self.pattern,
            data=data,
            is_leaf=True,
        )


class ListBlockParser:
    def __init__(self, order: bool = False) -> None:
        self.order = order
        self.begin_blank = re.compile(r"^\s*", re.M)
        if order:
            self.icon_pattern = re.compile(
                r"(?m:^)"  # match start of line
                r"(?P<icon>\d{1,3}\.\s+)"  # match list icon: 1. 2. 3.
                r" +",  # match one or more spaces after list icon
                re.VERBOSE,
            )

        else:
            self.icon_pattern = re.compile(
                r"(?m:^)"  # match start of line
                r"(?P<icon>[\*\+-]\s+)"  # match list icon: + or - or *
                r" +",  # match one or more spaces after list icon
                re.VERBOSE,
            )
            self.task_pattern = re.compile(r"^\[(?P<status>.*?)\] ")

    def __call__(self, text: str) -> tuple[str | None, ASTnode | None, str | None]:
        text = preprocess(text, end="")
        parts = re.split(r"(\n+)", text)
        lines = parts[::2]
        line_breaks = parts[1::2]

        forward, raw, raw_item, backward = "", [], "", ""
        flag_area, head_icon, head_icons, flag_icons = "forward", None, [], []

        for line, brk in zip_longest(lines, line_breaks, fillvalue=""):
            if flag_area == "forward":
                icon_match = self.icon_pattern.search(line)
                if icon_match:
                    flag_area = "content"
            elif flag_area == "content":
                icon_match = self.icon_pattern.search(line)
                if not (
                    icon_match
                    or line.startswith("  ")
                    or line.startswith("\t")
                    or line.strip() == ""
                ):
                    flag_area = "backward"

            # NOTE: when flag_area is "content", we certainly have icon_match
            if flag_area == "content":
                if icon_match:
                    head_icon = icon_match.group("icon")
                    head_icons.append(head_icon)
                line = line[len(head_icon) :]
                if (not self.order) and icon_match:  # unordered list may be task list
                    task_icon_match = self.task_pattern.search(line)
                    if task_icon_match:
                        flag_icons.append(task_icon_match.group("status"))
                        line = line[task_icon_match.end() :]

            if flag_area == "forward":
                forward += line + brk
            elif flag_area == "content":
                if icon_match and raw_item:
                    raw.append(raw_item)
                    raw_item = ""
                raw_item += line + brk
            elif flag_area == "backward":
                backward += line + brk

        if raw_item:
            raw.append(raw_item)

        if flag_area == "forward":
            return None, None, text

        forward = forward or None
        backward = backward or None
        return (
            forward,
            ASTnode(
                "list_block",
                pattern=None,  # self.pattern,
                raw=None,
                children=[
                    ASTnode("list_item", raw=item_raw.strip()) for item_raw in raw
                ],
                data={
                    "order": self.order,
                    "icons": head_icons,
                    "task_icons": flag_icons,
                },
            ),
            backward,
        )


class QuoteBlockParser(BlockParser):
    def __init__(self) -> None:
        self.pattern = re.compile(
            r"(?m:^)> "  # 匹配行首的>和空格
            r"(?!\[.+?\].*?\n)"  # 匹配category, 如![note]
            r"(?s:.)*?"  # 匹配content
            r"(?=((?m:^)[^>])|$)",
            re.VERBOSE,
        )
        self.line_start_pattern = re.compile(r"^> ", re.M)

    def get_ast_node(self, match: re.Match) -> ASTnode:
        raw = match.group()
        raw = self.line_start_pattern.sub(r"", raw)

        return ASTnode(
            "quote",
            pattern=self.pattern,
            raw=raw,
        )


class ParagraphParser:
    def __init__(self) -> None:
        self.pattern = re.compile(r"\n\s*\n")

    def __call__(self, text: str) -> tuple[None, list[ASTnode], None]:
        paragraphs = self.pattern.split(text)
        return (
            None,
            [ASTnode("paragraph", None, raw=para, is_leaf=True) for para in paragraphs],
            None,
        )


class HorizontalRuleParser(BlockParser):
    def __init__(self) -> None:
        self.pattern = re.compile(r"(?m:^)([-\*_]{3,}|\* \* \*|_ _ _|- - -)\s*\n")

    def get_ast_node(self, match: re.Match) -> ASTnode:
        return ASTnode(
            "horizontal_rule",
            pattern=self.pattern,
            raw=match.group(),
            is_leaf=True,
        )


class FootNoteParser(BlockParser):
    def __init__(self) -> None:
        self.pattern = re.compile(
            r"(?m:^)"
            r"(?P<content>\[\^.+?\]: "
            r"(?s:.)*?)"
            r"(?m:^)(?!(\ \ |\[\^.+?\]))"
        )
        self.key_pattern = re.compile(
            r"(?m:^)\[\^(?P<key>.+?)\]: (?P<content>(?s:.)*?)(?=(?m:^)\[\^.+?\]: |$)"
        )

    def get_ast_node(self, match: re.Match) -> ASTnode:
        content = match.group("content")
        res = self.key_pattern.findall(content)
        return ASTnode(
            "footnote",
            pattern=self.pattern,
            data={k: v for k, v in res},
            is_leaf=True,
        )


class CommentsBlockParser(BlockParser):
    def __init__(self) -> None:
        self.pattern = re.compile(r"(?m:^)%%(?P<content>(?s:.)*?)(?m:^)%%")

    def get_ast_node(self, match: re.Match) -> ASTnode:
        return ASTnode(
            "comment",
            pattern=self.pattern,
            raw=match.group("content"),
            is_leaf=True,
        )


class TableParser(BlockParser):
    def __init__(self) -> None:
        self.pattern = re.compile(
            r"(?m:^)(?P<header>.*?)\n"
            r"(?m:^)(?P<header_sep>\|?(?:\s*:?-+:?\s*\|)*?\s*:?-+:?\s*\|?)\n"
            r"(?m:^)(?P<content>(?s:.)*?)((?m:$)|$)"
            r"(?=((?m:^)[^|]*?(?m:$)))"
        )

    def get_ast_node(self, match: re.Match) -> ASTnode:
        header = match.group("header")
        headers = [s.strip() for s in header.strip("| ").split("|")]

        header_sep = match.group("header_sep")
        seps = [s.strip() for s in header_sep.strip("| ").split("|")]
        aligns = []
        for sep in seps:
            if sep.startswith(":") and sep.endswith(":"):
                aligns.append("center")
            elif sep.endswith(":"):
                aligns.append("right")
            else:
                aligns.append("left")

        node = ASTnode(
            "table",
            pattern=self.pattern,
            data={"header": headers, "align": aligns},
            is_leaf=False,
        )

        content = match.group("content").strip("\n")
        for row in content.split("\n"):
            for s in row.strip("| ").split("|"):
                node.children.append(ASTnode("table_cell", raw=s.strip()))

        return node
