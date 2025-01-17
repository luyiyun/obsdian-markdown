from obsidian_markdown.block_parser import SectionParser


def test_base_section_parse(test_data: dict[str, str]):
    content = test_data["section_base"]
    parser_1 = SectionParser(level=1)
    parser_2 = SectionParser(level=2)

    before, node, content2 = parser_1(content)
    assert before.strip() == ""
    assert node.name == "section1"
    assert node.data["title"] == "Section 1"

    before, node2, after = parser_2(node.raw)
    assert before.strip() == "12345"
    assert node2.name == "section2"
    assert node2.data["title"] == "Subsection 1.1"
    assert node2.raw.strip() == "1234"
    assert after.strip() == ""

    before, node, after = parser_1(content2)
    assert before is None
    assert after.strip() == ""
    assert node.name == "section1"
    assert node.data["title"] == "Section 2"
    assert node.raw.strip() == "456"


def test_section_with_comment_parse(test_data: dict[str, str]):
    content = test_data["section_with_comment"]
    parser_1 = SectionParser(level=1)
    parser_2 = SectionParser(level=2)

    _, node, _ = parser_1(content)
    _, node2, _ = parser_2(node.raw)
    assert node2.name == "section2"
    assert node2.data["title"] == "Subsection 1.1"
    assert "```python\n# This is a comment\nprint(1234)\n```" in node2.raw
