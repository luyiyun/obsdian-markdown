from obsidian_markdown.block_parser import MathBlockParser


def test_base_quote_parse(test_data: dict[str, str]):
    content = test_data["math_block_base"]
    parser = MathBlockParser()
    before, node, after = parser(content)
    assert before.strip() == "aaaaaa"
    assert after.strip() == "cccccc"
    assert node.name == "math_block"
    assert node.raw == "\na = b + 2\n"
