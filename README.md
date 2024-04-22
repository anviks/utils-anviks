# utils-anviks

Useful decorators and functions for everyday Python programming.

## Features:
### Decorators:
- `@stopwatch` measures execution time of a function (upon being called) and prints the time taken in seconds to the console.
- `@read_file` reads file content and passes it to the decorated function.
- `@catch` catches exceptions from a function.
- `@memoize` caches function results (only works with one positional hashable argument).
- `@enforce_types` checks types of function arguments and return value (raises TypeError if types don't match).

### Functions:
- `b64encode` encodes a string to a base64 string a specified number of times.
- `b64decode` decodes a base64 string a specified number of times.
- `tm_snapshot_to_string` builds a readable string from the given `tracemalloc` snapshot.
- `parse_file_content` reads file content and parses it using the provided arguments. It is an alternative to the `@read_file` decorator.

## Installation
```bash
pip install utils-anviks
```

## Usage

```python
import tracemalloc
from utils_anviks import stopwatch, read_file, catch, memoize, enforce_types, b64encode, b64decode, \
    tm_snapshot_to_string, parse_file_content


@stopwatch
def some_function():
    pass


@read_file('file.txt')
def some_function(file_content):
    pass


@catch
def some_function():
    pass


@memoize
def some_function(n):
    pass


@enforce_types
def some_function(n: int) -> int:
    pass


b64encode('string', 3)  # 'WXpOU2VXRlhOVzQ9'
b64decode('WXpOU2VXRlhOVzQ9', 3)  # 'string'

tracemalloc.start()
arr = [i for i in range(1000000)]  # random memory allocation
snapshot = tracemalloc.take_snapshot()
tracemalloc.stop()
print(tm_snapshot_to_string(snapshot))

parse_file_content('file.txt', _class=int)  # [1, 2, 3, 4, 5]
```
