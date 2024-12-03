# utils-anviks

Useful decorators and functions for everyday Python programming.

## Features:
### Decorators:
- `@stopwatch` measures execution time of a function (upon being called) and prints the time taken in seconds to the console.
- `@catch` catches exceptions from a function.
- `@enforce_types` checks types of function arguments and return value (raises TypeError if types don't match).

### Functions:
- `parse_string` splits a string by separators and converts to the given type.
- `parse_file_content` same as `parse_string`, but parses file content instead of a string.
- `b64encode` encodes a string to a base64 string a specified number of times.
- `b64decode` decodes a base64 string a specified number of times.
- `dict_to_object` converts a dictionary to an object, based on given type argument.
- `tm_snapshot_to_string` builds a readable string from the given `tracemalloc` snapshot.

### Classes:
- `CaptureMalloc` captures memory allocations within a block of code (context manager).

## Installation
```bash
pip install utils-anviks
```

## Usage

```python
import time
import tracemalloc
from utils_anviks import stopwatch, catch, enforce_types, parse_string, parse_file_content, b64encode, b64decode, \
    dict_to_object, tm_snapshot_to_string, CaptureMalloc


@stopwatch
def foo():
    time.sleep(1.23)


@catch(TypeError, ZeroDivisionError)
def bar(n: int):
    return 1 / n


@enforce_types
def baz(n: int) -> int:
    pass


foo()  # Time taken by the function to execute is printed to the console
print(bar(0))  # Catches ZeroDivisionError and returns (1, [error object])
baz('string')  # Raises TypeError

print(parse_string('111,222,333\n64,59,13', ('\n', ','), int))  # [[111, 222, 333], [64, 59, 13]]
print(parse_file_content('file.txt', ('\n', ','), int))  # Same as above, but reads from a file

print(b64encode('string', 3))  # 'WXpOU2VXRlhOVzQ9'
print(b64decode('WXpOU2VXRlhOVzQ9', 3))  # 'string'

class Foo:
    a: int
    b: str
    
print(dict_to_object({'a': 1, 'b': 'string'}, Foo))  # Foo(a=1, b='string')

tracemalloc.start()
arr1 = [i for i in range(100_000)]  # Arbitrarily chosen memory allocation
snapshot = tracemalloc.take_snapshot()
tracemalloc.stop()
print(tm_snapshot_to_string(snapshot))

with CaptureMalloc() as cm:
    arr2 = [i for i in range(100_000)]  # Arbitrarily chosen memory allocation
print(cm.snapshot_string)

```
