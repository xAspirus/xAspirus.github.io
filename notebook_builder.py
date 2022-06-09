import os
from glob import iglob

from commonmark import commonmark  # type: ignore


def read_file(file: str):
    with open(file, "r") as fp:
        return fp.read()


def all_files_recursive(dirpath: str):
    return [f for f in iglob(f"{dirpath}/**", recursive=True) if os.path.isfile(f)]


def template(template_file: str, **kwargs):
    return read_file("build/" + template_file).format(**kwargs)


def build_page(markdown_file_path: str):
    return template(
        "templates/page.html",
        header=read_file("templates/header.html"),
        markdown=commonmark(read_file(markdown_file_path)),
    )


def build(notebook_path: str, output_path: str):
    for markdown_file in all_files_recursive(notebook_path):
        if not markdown_file.endswith(".md"):
            continue
        name = markdown_file.split("/")[-1:][0][:-3] + ".html"
        with open(f"{output_path}/{name}", "w") as fp:
            fp.write(build_page(markdown_file))


build("/home/Aspirus/public_notebook", "notebook")
