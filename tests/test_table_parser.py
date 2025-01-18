from obsidian_markdown.block_parser import TableParser


def test_base_table_parse(test_data: dict[str, str]):
    content = test_data["table_base"]
    parser = TableParser()
    before, node, after = parser(content)
    assert before.strip() == "aaa"
    assert after.strip() == "bbb"
    assert node.name == "table"
    assert node.data["header"] == ["First name", "Last name"]
    assert node.data["align"] == ["left", "left"]
    assert len(node.children) == 4
    for child, text in zip(node.children, ["Max", "Planck", "Marie", "Curie"]):
        assert child.name == "table_cell"
        assert child.raw == text


def test_one_col_table_parse(test_data: dict[str, str]):
    content = test_data["table_one_column"]
    parser = TableParser()
    before, node, after = parser(content)
    assert before is None
    assert after is None
    assert node.name == "table"
    assert node.data["header"] == ["First name"]
    assert node.data["align"] == ["left"]
    assert len(node.children) == 2
    for child, text in zip(node.children, ["Max", "Marie"]):
        assert child.name == "table_cell"
        assert child.raw == text


def test_simple_table_parse(test_data: dict[str, str]):
    content = test_data["table_simple"]
    parser = TableParser()
    before, node, after = parser(content)
    assert before.strip() == ""
    assert after.strip() == ""
    assert node.name == "table"
    assert node.data["header"] == ["First name", "Last name"]
    assert node.data["align"] == ["left", "left"]
    assert len(node.children) == 4
    for child, text in zip(node.children, ["Max", "Planck", "Marie", "Curie"]):
        assert child.name == "table_cell"
        assert child.raw == text


def test_table_align_parse(test_data: dict[str, str]):
    content = test_data["table_with_align"]
    parser = TableParser()
    before, node, after = parser(content)
    assert before is None
    assert after is None
    assert node.name == "table"
    assert node.data["header"] == [
        "Left-aligned text",
        "Center-aligned text",
        "Right-aligned text",
    ]
    assert node.data["align"] == ["left", "center", "right"]
    assert len(node.children) == 3
    for child in node.children:
        assert child.name == "table_cell"
        assert child.raw == "Content"
