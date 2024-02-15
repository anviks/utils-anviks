# Utilities by anviks

This package contains some useful functions and decorators.

### Features in `decorators.py`:
- `@stopwatch` decorator to measure execution time of a function
- `@read_data` decorator to read data from file and pass it to a function
- `@catch` decorator to catch exceptions, that can be raised by a function
- `@memoize` decorator to cache function results
- `@enforce_types` decorator to check types of function arguments and return value (raises TypeError if types don't match)

### Features in `b64coder.py`:
- `b64encode` function to encode a string to base64
- `b64decode` function to decode a base64 string to a readable string

### Features in `memory_profiler.py`:
- `display_tm_snapshot` displays the top memory allocations from a tracemalloc snapshot.

### Installation
```bash
pip install -i https://test.pypi.org/simple/ utils-anviks
```

### Usage
```python
from utils_anviks import *
```
