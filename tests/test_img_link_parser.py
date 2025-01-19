from obsidian_markdown.block_parser import ImageLinkParser


def test_base_img_link_parse(test_data: dict[str, str]):
    content = test_data["img_link_base"]
    parser = ImageLinkParser()
    before, node, after = parser(content)
    assert before.strip() == "AAAA"
    assert node.name == "image_link"
    assert node.data["wiki"]
    assert node.data["link"] == "BBBB.png"
    assert node.data["category"] == "img"
    assert "width" not in node.data
    assert "position" not in node.data

    before, node, after = parser(after)
    assert before is None
    assert node.name == "image_link"
    assert not node.data["wiki"]
    assert node.data["link"] == "BBBB.png"
    assert node.data["title"] == "BBBB"
    assert node.data["category"] == "img"

    assert after.strip() == "CCCC"


def test_img_link_width_parse(test_data: dict[str, str]):
    content = test_data["img_link_wiki_with_width"]
    parser = ImageLinkParser()
    _, node, _ = parser(content)
    assert node.name == "image_link"
    assert node.data["wiki"]
    assert node.data["link"] == "BBBB.png"
    assert node.data["category"] == "img"
    assert node.data["width"] == 300


def test_img_link_excalidraw_parse(test_data: dict[str, str]):
    content = test_data["img_link_excalidraw"]
    parser = ImageLinkParser()
    _, node, _ = parser(content)
    assert node.name == "image_link"
    assert node.data["wiki"]
    assert node.data["link"] == "BBBB.excalidraw"
    assert node.data["category"] == "excalidraw"
    assert node.data["width"] == 300
    assert node.data["position"] == "center"
