from .ast import ASTnode
from .block_parser import (
    FrontMatterParser,
    SectionParser,
    MathBlockParser,
    CalloutParser,
    ImageLinkParser,
    CodeBlockParser,
    ParagraphParser,
)


class ObsidianMarkdown:
    def __init__(self):
        self.block_parsers = (
            [
                FrontMatterParser(),
            ]
            + [SectionParser(i) for i in range(1, 6)]
            + [
                MathBlockParser(),
                CalloutParser(),
                ImageLinkParser(),
                CodeBlockParser(),
                ParagraphParser(),
            ]
        )

        # TODO: is_leaf of paragraph is true, so the inline parsers are not used
        self.line_parsers = []

    def parse(self, text: str, parent: ASTnode = None, append: bool = True):
        text = text.replace("\r\n", "\n")
        text = text.replace("\r", "\n")
        if not text.endswith("\n"):
            text += "\n"

        if parent is None:
            parent = ASTnode("root", None)  # root node

        parsers = (
            self.line_parsers if parent.name == "paragraph" else self.block_parsers
        )
        for parser in parsers:
            forward, nodes, backward = parser(text)
            if nodes is None:
                text = backward
                continue

            if isinstance(nodes, ASTnode):
                nodes = [nodes]

            if append:
                parent.children += nodes
            else:
                parent.children = nodes + parent.children

            for node in nodes:
                node.parent = parent
                if forward:
                    self.parse(forward, parent=parent, append=False)
                if backward:
                    self.parse(backward, parent=parent, append=True)

                if node.is_leaf:
                    continue

                nodes_next = node.children if node.children else node
                for nni in nodes_next:
                    self.parse(nni.raw, parent=nni, append=True)
                    nni.raw = None  # clear the raw text to avoid duplication

            # the text has to be parsered by one parser, so we can break here
            break

        return parent
