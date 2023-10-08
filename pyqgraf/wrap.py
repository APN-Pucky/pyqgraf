""" Wrap a qgraf model with illegal characters in the name. """
import codecs
import re

# The default begin and end strings for wrapping.
# These are chosen to be unlikely to appear in a model.
# The content between the begin and end strings is a hex representation of the
# original string.
DEFAULT_BEGIN = "i"
DEFAULT_END = "i"


def wrap(s):
    sstr = s.encode("utf-8")
    return str(int(sstr.hex(),16))

def dewrap(s):
    return codecs.decode(str(hex(int(s))[2:]), "hex").decode("utf-8")

def wrap_model(model, begin=DEFAULT_BEGIN, end=DEFAULT_END):
    """Wrap a qgraf model with illegal characters in the name."""
    wrap_dict = {}
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
                    wrap_dict[contents[i]] = begin +wrap(contents[i])+ end
                    contents[i] =  wrap_dict[contents[i]] 
            rs += (
                line[: line.index("[") + 1]
                + ",".join(contents)
                + line[line.index("]") :]
                + "\n"
            )
        else:
            rs += line
    # we need the wrap dict to be able to wrap the input for qgraf
    return rs, wrap_dict


def dewrap_all(str, wrap_dict=None, begin=DEFAULT_BEGIN, end=DEFAULT_END):
    if wrap_dict is None:
        for match in re.finditer(
            re.escape(begin) + r"([a-f0-9]+)" + re.escape(end), str
        ):
            str = str.replace(match.group(0), dewrap(match.group(1)))
    else:
        for key in wrap_dict:
            str = str.replace(wrap_dict[key], key)
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
