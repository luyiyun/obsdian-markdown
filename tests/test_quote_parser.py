from obsidian_markdown.block_parser import QuoteBlockParser


def test_base_quote_parse(test_data: dict[str, str]):
    content = test_data["quote_base"]
    parser = QuoteBlockParser()
    before, node, after = parser(content)
    assert before is None
    assert after.strip() == "123455"
    assert node.name == "quote"
    assert node.raw == "This is a quote.\n"


def test_quote_end_parse(test_data: dict[str, str]):
    content = test_data["quote_then_end"]
    parser = QuoteBlockParser()
    before, node, after = parser(content)
    assert before is None
    assert after.strip() == ""
    assert node.name == "quote"
    assert node.raw == "This is a quote."


def test_quote_multiline_parse(test_data: dict[str, str]):
    content = test_data["quote_multi_lines"]
    parser = QuoteBlockParser()
    before, node, after = parser(content)
    assert before is None
    assert after.strip() == ""
    assert node.name == "quote"
    assert node.raw == (
        "This is a quote.\n"
        "This is the second line of the quote.\n"
        "This is the third line of the quote.\n"
    )
