from typing import List

import pytest

from frontmatter_up_to_tags import reformat_frontmatter_and_add_tags, reformat_dataview


@pytest.mark.parametrize("intext, outtext", [
    (["---\n", "up: python\n", "---\n", "\n"], ["---\n", "---\n", "#python\n", "\n"]),
    (["---\n", "val1: zeug\n",  "---\n", "\n"], ["---\n", "val1: zeug\n",  "---\n", "\n"]),
    (["---\n", 'up: "funktionale programmierung"', "---\n", "\n"], ["---\n", "---\n", "#funktionale_programmierung\n", "\n"]),
    (["---\n", 'up: "funktionale programmierung\n", python', "---\n", "\n"], ["---\n", "---\n", "#funktionale_programmierung, #python\n", "\n"]),
    (["---\n", "val1: zeug\n", 'up: "funktionale programmierung\n", python', "---\n", "\n"], ["---\n", "val1: zeug\n",  "---\n", "#funktionale_programmierung, #python\n", "\n"])
])
def test_reformat_frontmatter_and_add_tags(intext: List[str], outtext: List[str]) -> None:
    assert reformat_frontmatter_and_add_tags(intext) == outtext


@pytest.mark.parametrize("intext, outtext", [
    (["```dataview\n", 'table where contains(up, "python")', "```\n", ""], ["```dataview\n", "table from #python\n", "```\n", "\n"]),
    (["```dataview\n", 'table where up="python"', "```\n", "\n"], ["```dataview\n", "table from #python\n", "```\n", "\n"]),
    (["```dataview\n", 'table where contains(up, "funktionale programmierung")', "```\n", "\n"], ["```dataview\n", "table from #funktionale_programmierung\n", "```\n", "\n"]),
    (["```dataview\n", 'table where contains(up, "funktionale programmierung")', "```\n", "\n"], ["```dataview\n", "table from #funktionale_programmierung\n", "```\n", "\n"]),
    (["```dataview\n", 'table library as "Library\n", tags as "Tags" where programmiersprache="python" and contains(up, "python")', "```\n", "\n"], ["```dataview\n", 'table library as "Library\n", tags as "Tags" from #python where programmiersprache="python"', "```\n", "\n"])
])
def test_reformat_dataview(intext: List[str], outtext: List[str]) -> None:
    assert reformat_dataview(intext) == outtext
