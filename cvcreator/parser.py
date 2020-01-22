"""
"""

__all__ = ["interpolate", "parse"]


def interpolate(outer, inner):
    """Interpolate text components together.

    +---------+--------+--------------------------------------------+
    | outer   | inner  | results                                    |
    +=========+========+============================================+
    | `<any>` | `""`   | `""`                                       |
    +---------+--------+--------------------------------------------+
    | `str`   | `str`  | `outer % inner`                            |
    +---------+--------+--------------------------------------------+
    | `str`   | `dict` | `outer % inner`                            |
    +---------+--------+----------+-----+---------------------------+
    | `str`   | `list` | `outer[0]+inner+outer[1]`                  |
    +---------+--------+------+----+----+----+----------+----+------+
    | `list`  | `list` | `o[0]+i[0]+o[1]+i[1]+o[1]..o[1]+i[n]+o[2]` |
    +---------+--------+------+----+----+----+----------+----+------+

    Combinations of input not listed are not supported.

    Args:
        outer (dict, list, str) : The outer part of the interpolate
        inner (list, str) : The inner part of the interpolate

    Returns:
        (str): The argument woven together.

    Examples:
        >>> print(interpolate("spam%s", "eggs"))
        spameggs
        >>> print(interpolate("spam%s", ""))
        <BLANKLINE>
        >>> print(interpolate(["pre", "in", "post"], ["1", "2", "3"]))
        pre1in2in3post
    """

    if not inner:
        return ""

    if isinstance(outer, str):
        try:
            out = outer % inner
        except:
            print(outer)
            print(inner)
            raise ValueError("Interpolation fail!")

    elif isinstance(outer, list):

        if isinstance(inner, dict):
            if not all([isinstance(i, str) for i in inner.values()]):
                for key, val in inner.items():
                    if not isinstance(val, str):
                        print(repr(key))
                        print(repr(val))
                        raise ValueError("Values in dict not properly vetted!")
            inner = [inner[k] for k in sorted(inner.keys())]

        if isinstance(inner, str):
            inner = [inner]

        if len(inner) == 1:
            out = outer[0] + inner[0] + outer[-1]
        elif len(inner) == 2:
            out = outer[0] + inner[0] + outer[-2] + inner[1] + outer[-1]
        else:
            li, lo = len(inner), len(outer)
            if li < lo-1:
                outer = outer[:1] + outer[-(lo-li):]
            elif li >= lo:
                outer = outer[:1] + [outer[1]]*(li-lo+1) + outer[1:]
            inner.append("")
            out = "".join([a for b in zip(outer, inner) for a in b])

    return out


def verify_structure(content, template, name):

    if isinstance(template, dict):
        if not isinstance(content, dict):
            raise ValueError("YAML element '%s' should be a dict or omitted." % name)


def parse(content, template):
    """Weave together to nested YAML-structures using a set of basic rules.

    Args:
        content (dist, list, str) : Nested content from user provided content
        template (dict, list, str) : Nested content from template
    """
    # Retrieve name out of scope
    if "Basic" in content:
        content["Name"] = content["Basic"]["Name"]

    # Fix scope for all A<n>
    if "Projects" in template[1] and "Projects" in content:
        projects = template[1]["Projects"][1]
        for a in content["Projects"].keys():
            projects[a] = projects["A"]
        del projects["A"]
    
    # Fix scope for all B<n> 
    if "Publications" in template[1] and "Publications" in content:
        publications = template[1]["Publications"][1]
        for b in content["Publications"].keys():
            publications[b] = publications["B"]
        del publications["B"]

    content = _parse(content, template, "global")
    content = content.replace("__perc__", "%")
    return content


def _parse(content, template, name):

    # final directive
    if isinstance(template, list) and len(template) >= 3:
        assert all([isinstance(t, str) for t in template])

        if isinstance(content, list):
            for i, c in zip(range(len(content)), content):
                content[i] = _parse(c, template, name)

        elif isinstance(content, dict):
            for key in sorted(content.keys()):
                content[key] = _parse(content[key], template, key)

        elif isinstance(content, (str, int, float)):
            content = str(content)

        else:
            print(content)
            assert False

        return interpolate(template, content)

    # directive on own line
    if isinstance(template, list) and len(template) == 2:

        directive, template = template

        if isinstance(content, dict):

            if isinstance(template, dict):

                for key in content.keys():
                    if key not in template:
                        raise ValueError(
                            "key '%s' not recognised in template." % key)

                for key in sorted(template.keys()):

                    if key not in content:
                        content[key] = ""
                    else:
                        content[key] = _parse(content[key], template[key], key)

            elif isinstance(template, list) and len(template) == 2:

                directive2, template = template
                keys = sorted(content.keys())
                for key in keys:
                    content[key] = _parse(content[key], template, key)

                content = [interpolate(directive2, [key, content[key]]) for key in keys]

            elif isinstance(template, list) and len(template) >= 3:

                keys = sorted(content.keys())
                for key in keys:
                    content[key] = _parse(content[key], template, key)

                content = [interpolate(template, [key, content[key]]) for key in keys]

            elif isinstance(template, (int, float, str)):
                raise ValueError(
                    "Template assumes no subcategory of %s\n%s" % (
                        name, template))

        elif isinstance(content, list):
            for i, c in zip(range(len(content)), content):
                content[i] = _parse(c, template, name)

        elif isinstance(content, (int, float, str)):
            content = str(content)
            if "%" in content:
                content = "__perc__".join(content.split("%"))

        else:
            assert False

        return interpolate(directive, content)

    if isinstance(template, (int, float, str)):
        template = str(template)

        if isinstance(content, dict):
            for key in content.keys():
                content[key] = _parse(content[key], template, key)

        elif isinstance(content, list):
            for i, c in zip(range(len(content)), content):
                content[i] = _parse(c, template, name)

        elif isinstance(content, (int, float, str)):
            content = str(content)
            if "%" in content:
                content = "__perc__".join(content.split("%"))

        return interpolate(template, content)

    print(name)
    print(content)
    print(template)
    assert False


if __name__ == "__main__":
    import doctest
    doctest.testmod()
