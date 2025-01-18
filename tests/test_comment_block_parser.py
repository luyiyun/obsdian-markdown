from obsidian_markdown.block_parser import CommentsBlockParser


def test_base_section_parse(test_data: dict[str, str]):
    content = test_data["comment_block_base"]

    parser = CommentsBlockParser()
    before, node, after = parser(content)
    assert before.strip() == "aaa"
    assert after.strip() == "bbb"
    assert node.name == "comment"
    assert (
        node.raw.strip()
        == "This is a block comment.\n\nBlock comments can span multiple lines."
    )
