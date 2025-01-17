from obsidian_markdown.block_parser import FootNoteParser


def test_base_footnote_parse(test_data: dict[str, str]):
    content = test_data["footnote_base"]
    parser = FootNoteParser()
    before, node, after = parser(content)
    assert before.strip() == "This is a simple footnote[^1]."
    assert after.strip() == "xxxxxxxxxx"
    assert node.name == "footnote"
    for k in ["1", "2", "note"]:
        assert k in node.data.keys()
    assert node.data["1"].strip() == "aaa"
    assert node.data["2"].strip() == "bbb\n  cccc"
    assert node.data["note"].strip() == "dddd"


def test_end_footnote_parse(test_data: dict[str, str]):
    content = test_data["footnote_end"]
    parser = FootNoteParser()
    before, node, after = parser(content)
    assert before.strip() == "This is a simple footnote[^1]."
    assert after is None
    assert node.name == "footnote"
    for k in ["1", "2", "note"]:
        assert k in node.data.keys()
    assert node.data["1"].strip() == "aaa"
    assert node.data["2"].strip() == "bbb\n  cccc"
    assert node.data["note"].strip() == "dddd"
