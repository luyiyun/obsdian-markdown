from obsidian_markdown.block_parser import ParagraphParser


def test_base_paragraph_parse(test_data: dict[str, str]):
    content = test_data["paragraph_base"]
    parser = ParagraphParser()
    before, node, after = parser(content)
    assert before is None
    assert node.raw == "AAAA\nBBBB\n"

    before, node, after = parser(after)
    assert before is None
    assert node.raw == "CCCC\n"

    before, node, after = parser(after)
    assert before is None
    assert node.raw == "DDDD\n"
    assert after is None
