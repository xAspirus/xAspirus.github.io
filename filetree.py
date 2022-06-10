import sys
import os


def tree(path, indent=0):
    indent_str = "    " * indent
    out = lambda x: print(indent_str + x)
    out("<ul>")
    for i in os.listdir(path):
        if os.path.isfile(path + "/" + i):
            out(f"<li>{i}</li>")
        else:
            out("<li>")
            out(f"<h5>{i}</h5>")
            tree(path + "/" + i, indent=indent + 1)
            out("</li>")
    out("</ul>")


tree(sys.argv[1])
