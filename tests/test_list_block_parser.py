from obsidian_markdown.block_parser import ListBlockParser, CodeBlockParser


class TestListBlockParser:
    def test_base_unordered_parse(self, test_data: dict[str, str]):
        content = test_data["unordered_list_block_base"]
        parser = ListBlockParser()
        for icon in ["-", "*", "+"]:
            text = content.replace("-", icon)
            before, node, after = parser(text)
            assert not before
            assert after.strip() == "123455"
            assert node.name == "list_block"
            assert len(node.children) == 3
            for child, line in zip(node.children, ["AAA", "BBB", "CCC"]):
                assert child.name == "list_item"
                assert child.raw == line

    def test_unordered_parse_with_indent_content(self, test_data: dict[str, str]):
        content = test_data["unordered_list_block_indented_content"]
        parser = ListBlockParser()
        for icon in ["-", "*", "+"]:
            text = content.replace("-", icon)
            _, node, _ = parser(text)
            assert node.name == "list_block"
            assert len(node.children) == 3
            for child, line in zip(
                node.children, ["aaa\n3456789", "bbb\n1234567", "cccc"]
            ):
                assert child.name == "list_item"
                assert child.raw == line

    def test_unordered_parse_with_nested_list(self, test_data: dict[str, str]):
        content = test_data["unordered_list_block_nest"]
        parser = ListBlockParser()
        _, node, _ = parser(content)
        assert node.name == "list_block"
        assert len(node.children) == 3
        for child, nitems in zip(node.children, [2, 2, 3]):
            _, node, _ = parser(child.raw)
            assert node.name == "list_block"
            assert len(node.children) == nitems

    def test_unordered_parse_with_code_block(self, test_data: dict[str, str]):
        content = test_data["unordered_list_block_with_code_block"]
        cb_parser = CodeBlockParser()
        parser = ListBlockParser()

        content = cb_parser.preprocess(content)
        _, node, _ = parser(content)
        assert node.name == "list_block"
        assert len(node.children) == 3
        assert "code_id" in node.children[0].raw
        assert "code_id" not in node.children[1].raw
        assert "code_id" in node.children[2].raw

        _, cb_node, _ = cb_parser(node.children[0].raw)
        assert cb_node.name == "code_block"
        assert cb_node.raw == 'print("Hello, world!")\n'
        assert cb_node.data["lang"] == "python"

        _, cb_node, _ = cb_parser(node.children[2].raw)
        assert cb_node.name == "code_block"
        assert cb_node.data["lang"] == "cpp"
        assert cb_node.raw == (
            "#include <iostream>\n"
            "using namespace std;\n"
            "int main() {\n"
            '  cout << "Hello, world!" << endl;\n'
            "  return 0;\n"
            "}\n"
        )
