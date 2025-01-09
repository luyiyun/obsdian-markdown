from obsidian_markdown.block_parser import CalloutParser


class TestCalloutParser:
    def test_parse_callouts(self):
        text = (
            "aaaaaa\n" "## title\n" "\n" "> [!warning] \n" "> bbbbbb\n" "\n" "cccccc\n"
        )
        cp = CalloutParser()
        before, node, after = cp(text)
        assert before.strip() == "aaaaaa\n## title"
        assert after.strip() == "cccccc"
        assert node.name == "callout"
        assert node.data == {
            "category": "warning",
            "collapse": "",
            "title": "",
        }
        assert node.raw == "bbbbbb"

    def test_parse_callouts_wo_cotent(self):
        text = "> [!note]+ callout title\n\n" "cccc\n"
        cp = CalloutParser()
        _, node, _ = cp(text)
        assert node.name == "callout"
        assert node.raw == ""

    def test_parse_callouts_wo_succeed(self):
        text = "> [!note]+ callout title\n"
        cp = CalloutParser()
        _, node, _ = cp(text)
        assert node.name == "callout"
        assert node.raw == ""

        text = "> [!note]+ callout title"
        cp = CalloutParser()
        _, node, _ = cp(text)
        assert node.name == "callout"
        assert node.raw == ""

    def test_parse_callouts_title(self):
        text = "> [!note]+ callout title\n\n" "cccc\n"
        cp = CalloutParser()
        _, node, _ = cp(text)
        assert node.data["title"] == "callout title"
        assert node.data["collapse"] == "+"

    def test_parse_callouts_collapse(self):
        text = "> [!note]+ callout title\n\n" "cccc\n"
        cp = CalloutParser()
        _, node, _ = cp(text)
        assert node.data["collapse"] == "+"

    def test_parse_callouts_nest(self):
        text = (
            "aaaaaa\n"
            "## title\n"
            "\n"
            "> [!warning] \n"
            "> bbbbbb\n"
            "> > [!note]- nested\n"
            "> > cccc\n"
            "\n"
            "cccccc\n"
        )
        cp = CalloutParser()
        _, node, _ = cp(text)
        assert node.name == "callout"
        assert node.data["category"] == "warning"
        assert node.raw == ("bbbbbb\n" "> [!note]- nested\n" "> cccc")

        _, node2, _ = cp(node.raw)
        assert node.name == "callout"
        assert node2.data["category"] == "note"
        assert node2.data["collapse"] == "-"
        assert node2.data["title"] == "nested"
        assert node2.raw == "cccc"
