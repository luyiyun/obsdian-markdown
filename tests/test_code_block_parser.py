from obsidian_markdown.block_parser import CodeBlockParser


def test_base_code_block_parse(test_data: dict[str, str]):
    content = test_data["code_block_base"]
    parser = CodeBlockParser()
    before, node, after = parser(content)
    assert before.strip() == "aaa"
    assert after.strip() == "bbb"
    assert node.name == "code_block"
    assert node.data["lang"] == "python"
    assert node.raw == 'print("Hello, world!")\n'
