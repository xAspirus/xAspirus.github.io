import os
from glob import iglob

import frontmatter  # type: ignore
import mistune  # type: ignore
from rich import print as rprint


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


def build_page(markdown_file_path: str):
    metadata, markdown = render_markdown(markdown_file_path)
    return template(
        "templates/page.html",
        **metadata,
        markdown=markdown,
    )


def build(notebook_path: str, output_path: str):
    rprint(
        f'[blue] * Building Folder: [yellow]"{notebook_path}"[/yellow]\n * Output: [yellow]"{output_path}"[/yellow]'
    )
    os.system(f"rm -rf ./{output_path}")
    os.system(f"mkdir ./{output_path}")
    for markdown_file in all_files_recursive(notebook_path):
        rprint(f'  - Building File: "{markdown_file}"')
        if not markdown_file.endswith(".md"):
            continue
        name = markdown_file.split("/")[-1:][0][:-3] + ".html"
        with open(f"./{output_path}/{name}", "w") as fp:
            fp.write(build_page(markdown_file))


build("/home/aspirus/public_notebook", "notebook")
