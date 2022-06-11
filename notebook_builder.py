import os
import sys
from glob import iglob
from pathlib import Path

import frontmatter  # type: ignore
import mistune  # type: ignore
from rich import print as rprint


def write_file(path: str, text: str):
    output_file = Path(path)
    output_file.parent.mkdir(exist_ok=True, parents=True)
    output_file.write_text(text)


def ftree(path, root, indent=0):
    ret = ""
    indent_str = "    " * indent
    out = lambda x: indent_str + x + "\n"
    ret += out("<ul>")
    for i in os.listdir(path):
        if os.path.isfile(path + "/" + i):
            ret += out(f'<li><a href="{root}/{i.replace(".md", ".html")}">{i}</a></li>')
        else:
            ret += out("<li>")
            ret += out(f"<h5>{i}</h5>")
            ret += ftree(path + "/" + i, root=root + "/" + i, indent=indent + 1)
            ret += out("</li>")
    ret += out("</ul>")
    return ret


def read_file(file: str):
    with open(file, "r") as fp:
        return fp.read()


MD = mistune.create_markdown(
    escape=False, plugins=["strikethrough", "table", "task_lists"]
)


def render_markdown(markdown_file_path: str) -> tuple[dict, str]:
    file = frontmatter.load(markdown_file_path)
    return file.metadata, MD(file.content)


def all_files_recursive(dirpath: str):
    return [f for f in iglob(f"{dirpath}/**", recursive=True) if os.path.isfile(f)]


def template(template_file: str, **kwargs):
    try:
        return read_file(template_file).format(**kwargs)
    except KeyError as e:
        rprint(f"[bright_red][Error] Missing Meta-Data value:[/bright_red] {e}")
        exit(1)


def build_page(markdown_file_path: str, tree: str):
    metadata, markdown = render_markdown(markdown_file_path)
    return template("templates/page.html", **metadata, markdown=markdown, tree=tree)


def build(notebook_path: str, output_path: str):
    rprint(
        f'[blue] * Building Folder: [yellow]"{notebook_path}"[/yellow]\n * Output: [yellow]"{output_path}"[/yellow]'
    )
    tree = ftree(notebook_path, root="/" + output_path)
    os.system(f"rm -rf ./{output_path}")
    os.system(f"mkdir ./{output_path}")
    for markdown_file in all_files_recursive(notebook_path):
        rprint(f'  - Building File: "{markdown_file}"')
        if not markdown_file.endswith(".md"):
            continue
        name = markdown_file.split("/")[-1:][0][:-3] + ".html"
        write_file(
            f"./{output_path}/{markdown_file[len(notebook_path):].replace('.md', '.html')}",
            build_page(markdown_file, tree),
        )


build("/home/aspirus/public_notebook", "notebook")
