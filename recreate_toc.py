from pathlib import Path


def recreate_toc(filename: Path) -> None:
    with open(filename, 'r') as inf:
        text = inf.read()
    keyword = text.split("<<toc-selective-expandable '")[1].split("'")[0]
    print(keyword)

    original_text = f"""<div class="tc-table-of-contents">

<<toc-selective-expandable '{keyword}'>>

</div>"""
    replace_text = f"""```dataview
table where contains(up, "{keyword}")
```"""
    replaced = text.replace(original_text, replace_text)
    with open(filename, 'w') as outf:
        outf.write(replaced)


if __name__ == "__main__":
    for file in Path.cwd().glob("*/*.md"):
        try:
            recreate_toc(file)
            print(f"recreated TOC in {file}")
        except IndexError:
            print(f"nothing to rename in {file}")
