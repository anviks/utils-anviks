from typing import Any, Callable, Generator, Generic, Literal, Protocol, Sequence, TypeVar, TypeGuard

from .cell import Cell


class Add(Protocol):
    def __add__(self, other: Any) -> Any: ...


class AddMul(Add, Protocol):
    def __mul__(self, other: Any) -> Any: ...


T = TypeVar('T')
R = TypeVar('R')
Addable = TypeVar('Addable', bound=Add)


def is_coord_sequence(obj: Any) -> TypeGuard[Sequence[int]]:
    return isinstance(obj, Sequence) and len(obj) == 2 and isinstance(obj[0], int) and isinstance(obj[1], int)


class Grid(Generic[T]):
    __slots__ = ('grid',)

    def __init__(self, grid: list[list[T]]):
        self.grid = grid

    @property
    def height(self):
        return len(self.grid)

    @property
    def width(self):
        return len(self.grid[0])

    @property
    def rows(self):
        return self.grid

    @property
    def columns(self):
        return [list(col) for col in zip(*self.grid)]

    def find(self, value: T) -> Generator[Cell, Any, None]:
        return (Cell(i, j) for i in range(self.height) for j in range(self.width) if self.grid[i][j] == value)

    def find_first(self, value: T) -> Cell | None:
        return next(self.find(value), None)

    def transpose(self) -> 'Grid[T]':
        return Grid([list(col) for col in zip(*self.grid)])

    def rotate_clockwise(self) -> 'Grid[T]':
        return Grid([list(col) for col in zip(*self.grid[::-1])])

    def rotate_counter_clockwise(self) -> 'Grid[T]':
        return Grid([list(col) for col in zip(*self.grid)][::-1])

    def neighbours(self, cell: Cell, neighbour_type: Literal['cardinal', 'diagonal', 'all']) -> Generator[Cell, Any, None]:
        return (nb for nb in cell.neighbours(neighbour_type) if nb in self)

    def neighbour_directions(self, cell: Cell, neighbour_type: Literal['cardinal', 'diagonal', 'all']) -> Generator[tuple[int, int], Any, None]:
        return (direction for direction in cell.neighbour_directions(neighbour_type) if cell + direction in self)

    def copy(self) -> 'Grid':
        return Grid([row[:] for row in self.grid])

    def items(self) -> Generator[tuple[Cell, T], Any, None]:
        for i in range(self.height):
            for j in range(self.width):
                yield Cell(i, j), self.grid[i][j]

    def map(self, func: Callable[[Cell, T], R]) -> 'Grid[R]':
        new_grid = Grid.fill(self.height, self.width, None)

        for i in range(self.height):
            for j in range(self.width):
                new_grid.grid[i][j] = func(Cell(i, j), self.grid[i][j])

        return new_grid

    def apply(self, func: Callable[[Cell, T], None]) -> None:
        for cell, value in self.items():
            func(cell, value)

    def join_to_str(self, column_sep: str = '', row_sep: str = '\n') -> str:
        s = ''
        for row in self.grid:
            s += column_sep.join(map(str, row)) + row_sep
        return s

    def get(self, cell: Sequence[int] | Cell | int, default: T = None) -> T:
        if cell in self:
            return self[cell]
        return default

    def __getitem__(self, cell: Sequence[int] | Cell | int) -> T:
        if isinstance(cell, int):
            return self.grid[cell]
        if is_coord_sequence(cell):
            return self.grid[cell[0]][cell[1]]
        if isinstance(cell, Cell):
            return self.grid[cell.row][cell.column]
        raise TypeError(f'Invalid index type: {type(cell)}')

    def __setitem__(self, key: Cell | Sequence[int | Sequence[int] | Cell], value: T):
        if is_coord_sequence(key):
            self.grid[key[0]][key[1]] = value
        elif isinstance(key, Cell):
            self.grid[key.row][key.column] = value
        elif isinstance(key, Sequence):
            if len(key) == 0:
                return
            if is_coord_sequence(key[0]):
                for cell in key:
                    self.grid[cell[0]][cell[1]] = value
            elif isinstance(key[0], Cell):
                for cell in key:
                    self.grid[cell.row][cell.column] = value
            else:
                raise TypeError(f'Invalid index type: {type(key[0])}')
        elif isinstance(key, slice):
            if isinstance(key.start, Cell) and isinstance(key.stop, Cell):
                for i in range(min(key.start.row, key.stop.row), max(key.start.row, key.stop.row) + 1):
                    for j in range(min(key.start.column, key.stop.column), max(key.start.column, key.stop.column) + 1):
                        self.grid[i][j] = value
            else:
                raise TypeError(f'Invalid index type, both start and stop must be Cell instances: {type(key.start)}, {type(key.stop)}')
        else:
            raise TypeError(f'Invalid index type: {type(key)}')

    def __contains__(self, item: Sequence[int] | Cell) -> bool:
        if is_coord_sequence(item):
            item1, item2 = item
        elif isinstance(item, Cell):
            item1, item2 = item.row, item.column
        else:
            raise TypeError(f'Invalid index type: {type(item)}')
        return 0 <= item1 < self.height and 0 <= item2 < self.width

    def __iter__(self):
        return (cell for row in self.grid for cell in row)

    def __repr__(self):
        s = 'Grid(\n'
        for row in self.grid:
            s += f'    {row},\n'
        return s + ')'

    def __eq__(self, other):
        return self.grid == other.grid

    @staticmethod
    def arange(rows: int, columns: int, start: T, step: T) -> 'Grid[T]':
        return Grid([[start + step * (i * columns + j) for j in range(columns)] for i in range(rows)])

    @staticmethod
    def fill(rows: int, columns: int, value: T) -> 'Grid[T]':
        return Grid([[value] * columns for _ in range(rows)])

    @staticmethod
    def checkered(rows: int, columns: int, values: tuple[T, T]) -> 'Grid[T]':
        return Grid([[values[(i + j) % 2] for j in range(columns)] for i in range(rows)])

    @staticmethod
    def from_function(rows: int, cols: int, func: Callable[[int, int], T]) -> 'Grid[T]':
        return Grid([[func(i, j) for j in range(cols)] for i in range(rows)])

    @staticmethod
    def gradient(
            rows: int,
            cols: int,
            start: T,
            end: T,
            direction: Literal['horizontal', 'vertical', 'diagonal']
    ) -> 'Grid[T]':
        diff = end - start

        if direction == 'horizontal':
            func = lambda i, j: start + diff * j / (cols - 1)
        elif direction == 'vertical':
            func = lambda i, j: start + diff * i / (rows - 1)
        elif direction == 'diagonal':
            func = lambda i, j: start + diff * (i + j) / (rows + cols - 2)
        else:
            raise ValueError(f'Invalid direction: {direction}')

        return Grid.from_function(rows, cols, func)

    @staticmethod
    def gradient_by_step(
            rows: int,
            cols: int,
            start: Addable,
            step: AddMul,
            direction: Literal['horizontal', 'vertical', 'diagonal']
    ) -> 'Grid[Addable]':
        if isinstance(start, str):
            add = lambda x, y: chr(ord(x) + y)
        else:
            add = lambda x, y: x + y

        if direction == 'horizontal':
            func = lambda i, j: add(start, step * j)
        elif direction == 'vertical':
            func = lambda i, j: add(start, step * i)
        elif direction == 'diagonal':
            func = lambda i, j: add(start, step * (i + j))
        else:
            raise ValueError(f'Invalid direction: {direction}')

        return Grid.from_function(rows, cols, func)
