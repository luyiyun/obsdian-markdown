from obsidian_markdown.block_parser import ParagraphParser


def test_base_paragraph_parse(test_data: dict[str, str]):
    content = test_data["paragraph_base"]
    parser = ParagraphParser()
    _, nodes, _ = parser(content)
    assert isinstance(nodes, list)
    assert len(nodes) == 3
    nodes[0].raw == "AAAA\nBBBB"
    nodes[1].raw == "CCCC"
    nodes[2].raw == "DDDD"
