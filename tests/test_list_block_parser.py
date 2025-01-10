from obsidian_markdown.block_parser import ListBlockParser


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
        print(test_data)
        content = test_data["unordered_list_block_indented_content"]
        parser = ListBlockParser()
        for icon in ["-", "*", "+"]:
            text = content.replace("-", icon)
            _, node, _ = parser(text)
            assert node.name == "list_block"
            assert len(node.children) == 3
            for child, line in zip(
                node.children, ["aaa\n  3456789", "bbb\n  1234567", "cccc"]
            ):
                assert child.name == "list_item"
                assert child.raw == line
