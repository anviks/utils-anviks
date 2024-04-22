def parse_file_content(filename: str, *, sep: str = "\n", sep2: str | None = None, sep3: str | None = None,
                       _class: type = str):
    """
    Read file contents and parse them.

    The data will be read from the file with the given filename.
    The data will be split by the given separator (default: newline).
    If the data is two-dimensional, the second dimension will be split by the given separator (default: None).
    If the data is three-dimensional, the third dimension will be split by the given separator (default: None).
    The data will be converted to the given type (default: str) and returned.

    :param filename: The name of the file to read the data from.
    :param sep: The separator to split the data by.
    :param sep2: The separator of the second dimension or None.
    :param sep3: The separator of the third dimension or None.
    :param _class: The type to convert the data to.
    :return: Inner function.
    :raises ValueError: If the higher dimension separators are specified without the lower dimension separators.
    """
    if sep3 is not None and sep2 is None \
            or sep2 is not None and sep is None:
        raise ValueError(
            "Higher dimension separators cannot be specified if the lower dimension separators are not specified")

    with open(filename) as file:
        lines = file.read().split(sep)

    if sep2 is None:
        if _class == str:
            processed_data = lines
        else:
            processed_data = [_class(row) for row in lines]
    else:
        if sep2 == "":
            split_lines = [list(line) for line in lines]
        else:
            split_lines = [line.split(sep2) for line in lines]

        if sep3 is None:
            if _class == str:
                processed_data = split_lines
            else:
                processed_data = [
                    [_class(element) for element in row]
                    for row in split_lines
                ]
        else:
            if sep3 == "":
                split_lines = [[list(column) for column in row] for row in split_lines]
            else:
                split_lines = [[column.split(sep3) for column in row] for row in split_lines]

            if _class == str:
                processed_data = split_lines
            else:
                processed_data = [
                    [
                        [_class(element) for element in column]
                        for column in row
                    ]
                    for row in split_lines
                ]

    return processed_data
