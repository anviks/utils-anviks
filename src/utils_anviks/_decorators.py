"""Utility decorators for Python."""
import inspect
import sys
import time
import typing
import warnings
from functools import wraps


def stopwatch(func):
    """
    Print the runtime of a function.

    It will be printed out like: "It took [time] seconds for [function_name] to run",
    where [time] is the number of seconds (with the precision of at least 5 decimal places)
    it took for the function to run and [function_name] is the name of the function.
    The function's return value will not be affected.

    :param func: The decorated function.
    :return: Inner function.
    """
    recursion_counter = 0
    start = 0

    @wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal recursion_counter, start

        if recursion_counter == 0:
            start = time.perf_counter()

        recursion_counter += 1
        result = func(*args, **kwargs)
        recursion_counter -= 1

        if recursion_counter == 0:
            end = time.perf_counter()
            seconds = end - start
            print(f"It took {seconds} seconds for {func.__name__} to run")

        return result

    return wrapper


def memoize(func):
    """
    Cache the return value of a function.

    Memoization is an optimisation technique used primarily to speed up computer programs
    by storing the results of expensive function calls and returning the cached result
    when the same inputs occur again.
    For efficiency purposes, the wrapper function only takes one positional hashable argument.
    If this signature does not fit your use case, use the ``functools.cache`` decorator instead.

    :param func: The decorated function.
    :return: Inner function.
    """
    cache = {}

    @wraps(func)
    def wrapper(n):
        if n not in cache:
            cache[n] = func(n)
        return cache[n]

    return wrapper


def read_file(filename: str, *, sep: str = "\n", sep2: str | None = None, sep3: str | None = None, _class: type = str,
              auto_annotate: bool = False):
    """
    [DEPRECATED] Read file contents and pass them to the decorated function as the first argument.
    
    This decorator is deprecated in favor of the `parse_file_content` function. Please use `parse_file_content` instead.
    The reason for deprecation is that maintaining this as a decorator adds unnecessary complexity, especially for use with classes.
    The `parse_file_content` function provides equivalent functionality without the need for decoration and works universally.

    The data will be read from the file with the given filename.
    The data will be split by the given separator (default: newline).
    If the data is two-dimensional, the second dimension will be split by the given separator (default: None).
    If the data is three-dimensional, the third dimension will be split by the given separator (default: None).
    The data will be converted to the given type (default: str).
    The data will be passed to the decorated function as a list.

    :param filename: The name of the file to read the data from.
    :param sep: The separator to split the data by.
    :param sep2: The separator of the second dimension or None.
    :param sep3: The separator of the third dimension or None.
    :param _class: The type to convert the data to.
    :param auto_annotate: Whether to automatically add a type hint to the first parameter of the decorated function (default: False).
    It is done by modifying the source code of the decorated function's module, so its use is not recommended.
    :return: Inner function.
    :raises ValueError: If the higher dimension separators are specified without the lower dimension separators.
    """
    warnings.warn(
        "This decorator is deprecated in favor of the `parse_file_content` function. Please use `parse_file_content` instead.",
        DeprecationWarning, stacklevel=2)

    def decorator(func):
        if sep3 is not None and sep2 is None \
                or sep2 is not None and sep is None:
            raise ValueError(
                "Higher dimension separators cannot be specified if the lower dimension separators are not specified")

        if auto_annotate is True:
            if sys.version_info < (3, 9):
                from typing import List
                list_type = List
            else:
                list_type = list

            processed_type = list_type[_class]  # novermin
            if sep2 is not None:
                processed_type = list_type[processed_type]  # novermin
            if sep3 is not None:
                processed_type = list_type[processed_type]  # novermin

            funcs_module = inspect.getmodule(func)
            module_source_lines = inspect.getsourcelines(funcs_module)[0]
            func_source_lines, func_line_nr = inspect.getsourcelines(func)

            parameters = inspect.signature(func).parameters
            old_data_param = list(parameters.items())[0][1]
            new_data_param = old_data_param.replace(annotation=processed_type)

            if old_data_param != new_data_param:
                for i in range(func_line_nr, len(module_source_lines)):
                    old_line = module_source_lines[i]
                    new_line = old_line.replace(str(old_data_param), str(new_data_param))

                    if new_line != old_line:
                        module_source_lines[i] = new_line

                        with open(funcs_module.__file__, "w") as f:
                            f.write("".join(module_source_lines))

                        break

        @wraps(func)
        def wrapper(*args, **kwargs):
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

            return func(processed_data, *args, **kwargs)

        return wrapper

    return decorator


def catch(*error_classes):
    """
    Catch the specified exceptions.

    If the function raises one of the specified exceptions, return a tuple of (1, exception_object),
    where exception_object is the caught exception. Otherwise, return a tuple of (0, result),
    where result is the result of the function.

    This decorator is able to handle the following cases:
    1. The decorator is used with no arguments, e.g. @catch. Such usage will catch all exceptions.
    2. The decorator is used with one argument, e.g. @catch(ValueError).
    3. The decorator is used with multiple arguments, e.g. @catch(KeyError, TypeError).
    :param error_classes: The exceptions to catch.
    :return: Inner function.
    """

    def inner(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                return 0, result
            except error_classes as e:
                return 1, e

        return wrapper

    if len(error_classes) == 1 and error_classes[0].__class__ != type:
        function = error_classes[0]
        error_classes = Exception
        return inner(function)

    return inner


def enforce_types(func):
    """
    Enforce the types of the function's parameters and return value.

    If the function is called with an argument of the wrong type, raise a TypeError with the message:
    "Argument '[argument_name]' must be of type [expected_type], but was [value] of type [actual_type]".
    If the function returns a value of the wrong type, raise a TypeError with the message:
    "Returned value must be of type [expected_type], but was [value] of type [actual_type]".

    If an argument or the return value can be of multiple types, then the [expected_type]
    in the error message will be "[type_1], [type_2], ..., [type_(n-1)] or [type_n]".
    For example if the type annotation for an argument is int | float | str | bool, then the error message will be
    "Argument '[argument_name]' must be of type int, float, str or bool, but was [value] of type [actual_type]".

    If there's no type annotation for a parameter or the return value, then it can be of any type.

    Exceptions, that happen during the execution of the function still occur normally,
    if the argument types are correct.
    :param func: The decorated function.
    :return: Inner function.
    :raises TypeError: If the function is called with an argument of the wrong type or returns a value of the wrong type.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        sig = inspect.signature(func)
        bound = sig.bind(*args, **kwargs)
        err_message_arg = "Argument '{}' must be of type {}, but was {} of type {}"
        err_message_return = "Returned value must be of type {}, but was {} of type {}"

        for name, val in bound.arguments.items():
            if name in func.__annotations__:
                expected_type = func.__annotations__[name]
                verify_type(err_message_arg, expected_type, val, name)

        result = func(*args, **kwargs)

        if (expected_type := func.__annotations__.get("return", 0)) != 0:
            verify_type(err_message_return, expected_type, result)

        return result

    def verify_type(err_message, expected_type, value, parameter_name=None):
        if expected_type is None:
            expected_type = type(None)
        if not isinstance(value, expected_type):
            if typing.get_origin(expected_type) is typing.Union:
                exp_types = tuple(t.__name__ for t in expected_type.__args__)
                expected_type = ', '.join(exp_types[:-1]) + " or " + exp_types[-1]
            else:
                expected_type = expected_type.__name__
            actual_type = type(value).__name__
            if isinstance(value, str):
                value = f"'{value}'"

            if parameter_name is None:
                raise TypeError(err_message.format(expected_type, value, actual_type))
            raise TypeError(err_message.format(parameter_name, expected_type, value, actual_type))

    return wrapper
