from pathlib import Path
from typing import Callable, List


def reformat_frontmatter_and_add_tags(text: List[str]) -> List[str]:
    tags = []
    new_text = []
    for line in text:
        if 'up: ' in line:
            tags.extend(line.split('up:')[1].split(','))
        elif tags and "---" in line:
            new_text.append(line)
            tags_prog = []
            for tag_raw in tags:
                tags_prog.append(tag_raw.strip().replace(" ", "_").replace('"', ''))
            tag_list = ", ".join([f'#{tag}' for tag in tags_prog])
            if not tag_list.endswith('\n'):
                tag_list += '\n'
            new_text.append(tag_list)
            tags = []
        else:
            new_text.append(line)
    return new_text


def reformat_dataview(text: List[str]) -> List[str]:
    new_text = []
    tags_to_sort_by = ""
    for line in text:
        if 'up=' in line:
            (tag_filter, tags_to_sort_by) = line.split('up="')
        elif 'contains(up' in line:
            (tag_filter, tags_to_sort_by) = line.split('contains(up,')
        elif tags_to_sort_by and tag_filter:
            tags_to_sort_by = tags_to_sort_by.strip().replace('"', '').replace(' ', '_').replace(')', '')
            tag_filter = tag_filter.strip()
            if tag_filter.endswith("where"):
                tag_filter = tag_filter.split('where')[0]
            if tag_filter.endswith("and"):
                tag_filter = tag_filter.split('and')[0]
                newline = tag_filter.split('where')
                tag_filter = newline[0] + f"from #{tags_to_sort_by} where" + newline[1].split('where')[0]
            else:
                tag_filter += f"from #{tags_to_sort_by}"
            new_text.append(tag_filter.strip())
            new_text.append(line)
            tag_filter = ""
            tags_to_sort_by = ""
        else:
            new_text.append(line)
    return new_text


def load_and_save_file(filename: Path, filterfunc: Callable):
    with open(filename, 'r') as infile:
        intext = infile.readlines()
    outtext = filterfunc(intext)
    with open(f"{filename}", 'w') as outfile:
        outfile.writelines(outtext)
    if intext == outtext:
        print(f"nothing to do for {filename}")
    else:
        print(f"callec {filterfunc.__name__} for {filename}")


if __name__ == "__main__":
    files = Path.cwd().glob("testbox_frontmatter_to_tags/*.md")
    filterfunctions = [
        reformat_frontmatter_and_add_tags,
        reformat_dataview
    ]
    for file in files:
        for function in filterfunctions:
            load_and_save_file(file, function)
