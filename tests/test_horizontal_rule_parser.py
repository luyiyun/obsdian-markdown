from obsidian_markdown.block_parser import HorizontalRuleParser


def test_base_quote_parse(test_data: dict[str, str]):
    content = test_data["horizontal_rule"]
    parser = HorizontalRuleParser()
    before, node, after = parser(content)
    assert before is None
    assert node.name == "horizontal_rule"
    assert node.raw.strip() == "***"

    _, node, after = parser(after)
    assert node.name == "horizontal_rule"
    assert node.raw.strip() == "****"

    _, node, after = parser(after)
    assert node.name == "horizontal_rule"
    assert node.raw.strip() == "* * *"

    _, node, after = parser(after)
    assert node.name == "horizontal_rule"
    assert node.raw.strip() == "---"

    _, node, after = parser(after)
    assert node.name == "horizontal_rule"
    assert node.raw.strip() == "----"

    _, node, after = parser(after)
    assert node.name == "horizontal_rule"
    assert node.raw.strip() == "- - -"

    _, node, after = parser(after)
    assert node.name == "horizontal_rule"
    assert node.raw.strip() == "___"

    _, node, after = parser(after)
    assert node.name == "horizontal_rule"
    assert node.raw.strip() == "____"

    _, node, after = parser(after)
    assert node.name == "horizontal_rule"
    assert node.raw.strip() == "_ _ _"
