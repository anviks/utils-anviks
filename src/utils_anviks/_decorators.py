"""Utility decorators for Python."""
import inspect
import time
import typing
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
