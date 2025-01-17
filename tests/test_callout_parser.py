from obsidian_markdown.block_parser import CalloutParser, CodeBlockParser


class TestCalloutParser:
    def test_parse_callouts(self, test_data: dict[str, str]):
        text = test_data["callout_base"]
        cp = CalloutParser()
        before, node, after = cp(text)
        assert before.strip() == "aaaaaa\n\n## title"
        assert after.strip() == "cccccc"
        assert node.name == "callout"
        assert node.data == {
            "category": "warning",
            "collapse": "",
            "title": "",
        }
        assert node.raw == "bbbbbb"

    def test_parse_callouts_wo_content(self, test_data: dict[str, str]):
        text = test_data["callout_wo_content"]
        cp = CalloutParser()
        _, node, _ = cp(text)
        assert node.name == "callout"
        assert node.raw == ""

    def test_parse_callouts_wo_succeed(self, test_data: dict[str, str]):
        text = test_data["callout_wo_succeed"]
        cp = CalloutParser()
        _, node, _ = cp(text)
        assert node.name == "callout"
        assert node.raw == ""

        text = "> [!note]+ callout title"
        cp = CalloutParser()
        _, node, _ = cp(text)
        assert node.name == "callout"
        assert node.raw == ""

    def test_parse_callouts_title(self, test_data: dict[str, str]):
        text = test_data["callout_title"]
        cp = CalloutParser()
        _, node, _ = cp(text)
        assert node.data["title"] == "callout title"
        assert node.data["collapse"] == "+"

    def test_parse_callouts_collapse(self, test_data: dict[str, str]):
        text = test_data["callout_collapse"]
        cp = CalloutParser()
        _, node, _ = cp(text)
        assert node.data["collapse"] == "+"

    def test_parse_callouts_nest(self, test_data: dict[str, str]):
        text = test_data["callout_nest"]
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

    # def test_parse_callouts_w_code(self, test_data: dict[str, str]):
    #     text = test_data["callout_code"]
    #     code_parser = CodeBlockParser()
    #     text = code_parser.preprocess(text)
    #     assert "([<@#$code_id 0&*%)]>" in text
    #
    #     cp = CalloutParser()
    #     _, node, _ = cp(text)
    #     assert node.name == "callout"
    #     assert node.data["category"] == "note"
    #
    #     before, node2, after = code_parser(node.raw)
    #     assert before.strip() == "bbbbbb"
    #     assert after.strip() == ""
    #     assert node2.name == "code_block"
    #     assert node2.data["lang"] == "python"
    #     assert node2.raw == 'print("Hello, world!")'
