from obsidian_markdown.block_parser import MathBlockParser


def test_base_math_block_parse(test_data: dict[str, str]):
    content = test_data["math_block_base"]
    parser = MathBlockParser()
    before, node, after = parser(content)
    assert before.strip() == "aaaaaa"
    assert after.strip() == "cccccc"
    assert node.name == "math_block"
    assert node.raw == "\na = b + 2\n"


def test_math_block_w_id_parse(test_data: dict[str, str]):
    content = test_data["math_block_w_identifier"]
    parser = MathBlockParser()
    before, node, after = parser(content)
    assert before.strip() == "aaaaaa"
    assert after.strip() == "cccccc"
    assert node.name == "math_block"
    assert node.raw == "\na = b + 2\n"
    assert node.data["id"] == "equ-example"
