"""Merge configuration files."""

def merge_configurations(configurations):
    """
    Merge configuration files.

    Instead of a list of configurations, create a single configuration, where
    the leaf-nodes are merged. Missing values and duplicates are ignored.

    In addition, the sections ``Projects`` and ``Publications`` have special
    handle. Instead of keeping the ``A1, A2, ...``, structure, the elements are
    instead collapsed down to a list intact. In other words, projects and
    publications are not merged, but instead kept as a list.

    Args:
        configurations (Sequence[Dict[str, Any]]):
            Multiple raw loaded yaml configuration files.

    Returns:
        Merged version of ``configurations``

    Examples:
        >>> merge_configurations([{"Basic": {"Name": "name1"}},
        ...                       {"Basic": {"Name": "name2"}}])
        {'Basic': {'Name': ['name1', 'name2']}}
        >>> merge_configurations([{"Skills": {"Languages": ["C", "Python"]}},
        ...                       {"Skills": {"Languages": ["C", "Bash"]}}])
        {'Skills': {'Languages': ['Bash', 'C', 'Python']}}
        >>> merge_configurations([  # doctest: +NORMALIZE_WHITESPACE
        ...     {"Projects": {"A1": {"Activity": "fighting"}}},
        ...     {"Projects": {"A1": {"Activity": "stealing"}}},
        ...     {"Projects": {"A2": {"Activity": "thuggin"}}}
        ... ])
        {'Projects': [{'Activity': 'fighting'},
                      {'Activity': 'stealing'},
                      {'Activity': 'thuggin'}]}

    """
    if isinstance(configurations[0], list):

        if isinstance(configurations[0][0], str):
            out = sorted(set(
                element for config in configurations for element in config))

        # Skip the elements on format ``start, [stop], description``
        # This covers first and foremost Education and Work.
        else:
            out = None

    elif isinstance(configurations[0], dict):
        keys = sorted(set(
            key for config in configurations for key in config.keys()))
        out = {}
        for key in keys:

            # Projects and Publications have an unnecessary extra layer that we
            # strip away. Content should not need merging.
            if key in ["Projects", "Publications"]:

                value = [
                    project
                    for config in configurations if key in config
                    for project in config[key].values()
                ]

            else:
                value = merge_configurations([config[key]
                                              for config in configurations
                                              if key in config])

            # Skip if nothing of value
            if value:
                out[key] = value

    elif isinstance(configurations[0], (int, float, str)):
        out = sorted(set(str(value) for value in configurations))

    else:
        raise ValueError(
            "I don't know how to handle the following input: %s" % configurations)

    return out
