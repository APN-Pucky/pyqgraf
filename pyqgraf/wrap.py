""" Wrap a qgraf model with illegal characters in the name. """
import codecs
import re

DEFAULT_BEGIN = "i"
DEFAULT_END = "i"


# src: https://stackoverflow.com/a/29026749
def wrap(s):
    str = s.encode("utf-8")
    return str.hex()


def dewrap(s):
    return codecs.decode(s, "hex").decode("utf-8")


def wrap_model(model, begin=DEFAULT_BEGIN, end=DEFAULT_END):
    """Wrap a qgraf model with illegal characters in the name."""
    chars = "".join(str(n) for n in range(10)) + "abcdefg"
    rs = ""
    for line in model.splitlines():
        if line.startswith("*"):
            continue
        if "[" in line and "]" in line:
            content = line[line.index("[") + 1 : line.index("]")]
            contents = content.split(",")
            for i in range(len(contents)):
                contents[i] = contents[i].strip()
            for i in range(len(contents)):
                if contents[i] != "+" and contents[i] != "-":
                    contents[i] = begin + wrap(contents[i]) + end
            rs += (
                line[: line.index("[") + 1]
                + ",".join(contents)
                + line[line.index("]") :]
            )
        else:
            rs += line
    return rs


def dewrap_all(str, begin=DEFAULT_BEGIN, end=DEFAULT_END):
    for match in re.finditer(
        re.escape(begin) + r"([a-f0-9]+)" + re.escape(end), str
    ):
        str = str.replace(match.group(0), dewrap(match.group(1)))
    return str


def dewrap_model(model, begin=DEFAULT_BEGIN, end=DEFAULT_END):
    """Dewrap a qgraf model with illegal characters in the name."""
    chars = "".join(str(n) for n in range(10)) + "abcdefg"
    rs = ""
    for line in model.splitlines():
        if line.startswith("*"):
            continue
        if "[" in line and "]" in line:
            content = line[line.index("[") + 1 : line.index("]")]
            contents = content.split(",")
            for i in range(len(contents)):
                contents[i] = contents[i].strip()
            for i in range(len(contents)):
                if contents[i] != "+" and contents[i] != "-":
                    contents[i] = dewrap(contents[i][len(begin) : -len(end)])
            rs += (
                line[: line.index("[") + 1]
                + ",".join(contents)
                + line[line.index("]") :]
            )
        else:
            rs += line
    return rs
