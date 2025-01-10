from .ast import ASTnode
from .block_parser import (
    FrontMatterParser,
    SectionParser,
    MathBlockParser,
    CalloutParser,
    ImageLinkParser,
    CodeBlockParser,
)
from .utils import preprocess


class ObsidianMarkdown:
    def __init__(self):
        self.block_parsers_w_preproc = [CodeBlockParser()]
        self.block_parsers = (
            [
                FrontMatterParser(),
            ]
            + [SectionParser(i) for i in range(1, 6)]
            + [MathBlockParser(), CalloutParser(), ImageLinkParser()]
            + self.block_parsers_w_preproc
            + [
                lambda text: (
                    None,
                    ASTnode("paragraph", None, raw=preprocess(text), is_leaf=True),
                    None,
                ),  # default parser
            ]
        )

        # TODO: is_leaf of paragraph is true, so the inline parsers are not used
        self.inline_parsers = []

    def parse(self, text: str, parent: ASTnode = None, append: bool = True):
        if parent is None:
            parent = ASTnode("root", None)  # root node

        if parent.name == "paragraph":
            parsers = self.inline_parsers
        else:
            parsers = self.block_parsers
            # NOTE: 一些嵌套在其他块级结构中的代码块，比如再callout中的代码块，
            # 因为前面前面可能存在'> '，这导致其无法被第一次parser处理，需要重新处理一下
            for parser in self.block_parsers_w_preproc:
                text = parser.preprocess(text)

        for parser in parsers:
            forward, node, backward = parser(text)
            if node is not None:
                node.parent = parent
                if append:
                    parent.children.append(node)
                else:
                    parent.children.insert(0, node)
                if forward:
                    self.parse(forward, parent=parent, append=False)
                if backward:
                    self.parse(backward, parent=parent, append=True)
                if not node.is_leaf:
                    if not node.children:  # empty
                        self.parse(node.raw, parent=node, append=True)
                        node.raw = None  # clear the raw text to avoid duplication
                    else:
                        for child in node.children:
                            if child.is_leaf:
                                continue
                            self.parse(child.raw, parent=child, append=True)
                break
            else:
                text = backward

        return parent
