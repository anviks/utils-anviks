from typing import Literal


class Cell:
    """Represents a location in a 2-dimensional grid."""

    __slots__ = ('row', 'column')

    def __init__(self, row: int, column: int): ...

    @property
    def row(self) -> int:
        """Get the row coordinate of this cell."""
        ...

    @property
    def column(self) -> int:
        """Get the column coordinate of this cell."""
        ...

    @property
    def up(self) -> Cell:
        """Get the cell above this cell."""
        ...

    @property
    def down(self) -> Cell:
        """Get the cell below this cell."""
        ...

    @property
    def left(self) -> Cell:
        """Get the cell to the left of this cell."""
        ...

    @property
    def right(self) -> Cell:
        """Get the cell to the right of this cell."""
        ...

    def neighbours(self, neighbour_type: Literal['cardinal', 'diagonal', 'all'], /) -> tuple[Cell, ...]:
        """
        Get the neighbours of this cell.

        The ``neighbour_type`` parameter determines which neighbours are returned:
            - ``'cardinal'``: Includes top, bottom, left, and right neighbors.
            - ``'diagonal'``: Includes diagonal neighbors only.
            - ``'all'``: Includes both cardinal and diagonal neighbors.

        :param neighbour_type: The type of neighbours to consider.
        :return: A tuple of neighbouring cells.
        """
        ...

    def is_neighbour(self, other: Cell, neighbour_type: Literal['cardinal', 'diagonal', 'all'], /) -> bool:
        """
        Check if the other cell is a neighbour of this cell.

        The ``neighbour_type`` parameter determines which directions are returned:
            - ``'cardinal'``: Includes top, bottom, left, and right directions.
            - ``'diagonal'``: Includes diagonal directions only.
            - ``'all'``: Includes both cardinal and diagonal directions.

        :param other: The other cell.
        :param neighbour_type: The type of neighbours to consider.
        :return: True if the other cell is a neighbour, False otherwise.
        """
        ...

    def manhattan_distance(self, other: 'Cell', /) -> int:
        """
        Return the Manhattan distance between two cells.

        The Manhattan distance is the sum of the absolute differences between the row and column coordinates.
        In other words, it is the distance between two points if you could only move in cardinal directions.
        ::
                  -2  -1   0   1   2
                -----------------------
            -2  |  4   3   2   3   4  |
            -1  |  3   2   1   2   3  |
             0  |  2   1   X   1   2  |
             1  |  3   2   1   2   3  |
             2  |  4   3   2   3   4  |
                -----------------------

        :param other: The other cell.
        :return: The Manhattan distance between the two cells.
        """
        ...

    def euclidean_distance(self, other: 'Cell', /) -> float:
        """
        Return the Euclidean distance between two cells.

        The Euclidean distance is the straight-line distance between two points.
        ::
                    -2  -1   0   1   2
                -----------------------
            -2  |  2.8 2.2 2.0 2.2 2.8 |
            -1  |  2.2 1.4 1.0 1.4 2.2 |
             0  |  2.0 1.0  X  1.0 2.0 |
             1  |  2.2 1.4 1.0 1.4 2.2 |
             2  |  2.8 2.2 2.0 2.2 2.8 |
                -----------------------

        :param other: The other cell.
        :return: The Euclidean distance between the two cells.
        """
        ...

    def chebyshev_distance(self, other: 'Cell', /) -> int:
        """
        Return the Chebyshev distance between two cells.

        The Chebyshev distance is the maximum of the absolute differences between the row and column coordinates.
        In other words, it is the distance between two points if you could move in cardinal and diagonal directions.
        ::
                  -2  -1   0   1   2
                -----------------------
            -2  |  2   2   2   2   2  |
            -1  |  2   1   1   1   2  |
             0  |  2   1   X   1   2  |
             1  |  2   1   1   1   2  |
             2  |  2   2   2   2   2  |
                -----------------------

        :param other: The other cell.
        :return: The Chebyshev distance between the two cells.
        """
        ...

    @staticmethod
    def neighbour_directions(neighbour_type: Literal['cardinal', 'diagonal', 'all'], /) -> tuple[tuple[int, int], ...]:
        """
        Get the directions of the neighbours of this cell.

        The ``neighbour_type`` parameter determines which directions are returned:
            - ``'cardinal'``: Includes top, bottom, left, and right directions.
            - ``'diagonal'``: Includes diagonal directions only.
            - ``'all'``: Includes both cardinal and diagonal directions.

        :param neighbour_type: The type of neighbours to consider.
        :return: A tuple of directions.
        """
        ...

    def __add__(self, other: Cell | tuple[int, int] | complex): ...

    def __radd__(self, other: Cell | tuple[int, int] | complex): ...

    def __sub__(self, other: Cell | tuple[int, int] | complex): ...

    def __rsub__(self, other: Cell | tuple[int, int] | complex): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __complex__(self): ...

    def __iter__(self): ...

    def __hash__(self): ...

    def __repr__(self): ...
