from obsidian_markdown.block_parser import ListBlockParser, CodeBlockParser


def test_base_unordered_parse(test_data: dict[str, str]):
    content = test_data["unordered_list_block_base"]
    parser = ListBlockParser()
    for icon in ["-", "*", "+"]:
        text = content.replace("-", icon)
        before, node, after = parser(text)
        assert before is None
        assert after.strip() == "123455"
        assert node.name == "list_block"
        assert len(node.children) == 3
        assert not node.data["order"]
        assert not node.data["task_icons"]
        assert node.data["icons"] == [f"{icon} "] * 3
        for child, line in zip(node.children, ["AAA", "BBB", "CCC"]):
            assert child.name == "list_item"
            assert child.raw == line


def test_unordered_parse_with_indent_content(test_data: dict[str, str]):
    content = test_data["unordered_list_block_indented_content"]
    parser = ListBlockParser()
    for icon in ["-", "*", "+"]:
        text = content.replace("-", icon)
        _, node, _ = parser(text)
        assert node.name == "list_block"
        assert len(node.children) == 3
        for child, line in zip(node.children, ["aaa\n3456789", "bbb\n1234567", "cccc"]):
            assert child.name == "list_item"
            assert child.raw == line


def test_unordered_parse_with_nested_list(test_data: dict[str, str]):
    content = test_data["unordered_list_block_nest"]
    parser = ListBlockParser()
    _, node, _ = parser(content)
    assert node.name == "list_block"
    assert len(node.children) == 3
    for child, nitems in zip(node.children, [2, 2, 3]):
        _, node, _ = parser(child.raw)
        assert node.name == "list_block"
        assert len(node.children) == nitems


def test_unordered_parse_with_code_block(test_data: dict[str, str]):
    content = test_data["unordered_list_block_with_code_block"]
    cb_parser = CodeBlockParser()
    parser = ListBlockParser()

    _, node, _ = parser(content)
    assert node.name == "list_block"
    assert len(node.children) == 3

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


def test_base_ordered_parse(test_data: dict[str, str]):
    content = test_data["ordered_list_block_base"]
    parser = ListBlockParser(order=True)
    before, node, after = parser(content)
    assert before is None
    assert after.strip() == "123455"
    assert node.name == "list_block"
    assert node.data["order"]
    assert node.data["icons"] == ["1. ", "2. ", "3. "]
    assert len(node.children) == 3
    for child, line in zip(node.children, ["AAA", "BBB", "CCC"]):
        assert child.name == "list_item"
        assert child.raw == line


def test_ordered_parse_with_indent_content(test_data: dict[str, str]):
    content = test_data["ordered_list_block_indented_content"]
    parser = ListBlockParser(order=True)
    _, node, _ = parser(content)
    assert node.name == "list_block"
    assert len(node.children) == 3
    for child, line in zip(node.children, ["aaa\n3456789", "bbb\n1234567", "cccc"]):
        assert child.name == "list_item"
        assert child.raw == line


def test_ordered_parse_with_code_block(test_data: dict[str, str]):
    content = test_data["ordered_list_block_with_code_block"]
    cb_parser = CodeBlockParser()
    parser = ListBlockParser(order=True)

    _, node, _ = parser(content)
    assert node.name == "list_block"
    assert len(node.children) == 3

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


def test_ordered_parse_with_nested_list(test_data: dict[str, str]):
    content = test_data["ordered_list_block_nest"]
    parser = ListBlockParser(order=True)
    _, node, _ = parser(content)
    assert node.name == "list_block"
    assert len(node.children) == 3
    for child, nitems in zip(node.children, [2, 2, 3]):
        _, node, _ = parser(child.raw)
        assert node.name == "list_block"
        assert len(node.children) == nitems


def test_task_list_parse(test_data: dict[str, str]):
    content = test_data["task_list_base"]
    parser = ListBlockParser(order=False)
    _, node, _ = parser(content)
    assert node.name == "list_block"
    assert node.data["task_icons"] == [" ", " ", "x"]
    for child, line in zip(node.children, ["aaa", "bbb", "cccc"]):
        assert child.name == "list_item"
        assert child.raw == line
