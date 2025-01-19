from obsidian_markdown.block_parser import FrontMatterParser


def test_base_front_matter_parse(test_data: dict[str, str]):
    content = test_data["front_matter_base"]
    parser = FrontMatterParser()
    before, node, after = parser(content)
    assert before is None
    assert after.strip() == "1234"
    assert node.name == "front_matter"
    assert node.data["title"] == "Example"
    assert node.data["tags"] == ["tag1", "tag2", "tag3"]
    assert node.data["author"] == "admin"
    assert node.data["created"] == "2024-12-25 16:10"
    assert node.data["publish"]
