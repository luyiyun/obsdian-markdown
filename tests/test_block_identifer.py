from obsidian_markdown.block_parser import ParagraphParser


def test_block_identifier(test_data: dict[str, str]):
    content = test_data["identifier_base"]
    parser = ParagraphParser()
    _, node, after = parser(content)
    assert node.data["id"] == "abc"
    assert node.raw == "AAAA"
    assert after.startswith("BBBB")

    _, node, after = parser(after)
    assert node.data["id"] == "cdf"
    assert node.raw == "BBBB"
    assert after.strip() == ""


def test_block_identifier_dup(test_data: dict[str, str]):
    content = test_data["identifier_duplicate"]
    parser = ParagraphParser()
    _, node, after = parser(content)
    assert node.data["id"] == "abc"
    assert node.raw == "AAAA"

    assert after.startswith("^cdf")
