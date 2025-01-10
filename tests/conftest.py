import re
import pytest


@pytest.fixture
def test_data() -> dict[str, str]:
    with open("tests/example.md", "r") as f:
        text = f.read()
    res = re.findall(r"===(?P<name>.*?)===\n(.*?)===(?P=name)===", text, re.DOTALL)
    return {k: v for k, v in res}
