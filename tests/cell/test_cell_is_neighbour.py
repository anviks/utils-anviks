from utils_anviks.cell import Cell


def test_cell_is_cardinal_neighbour():
    cell = Cell(100, 100)

    cardinal_neighbours = {
        Cell(100, 99),
        Cell(100, 101),
        Cell(99, 100),
        Cell(101, 100),
    }

    for i in range(90, 111):
        for j in range(90, 111):
            other_cell = Cell(i, j)
            assert cell.is_neighbour(other_cell, 'cardinal') == (other_cell in cardinal_neighbours), \
                f"Expected {other_cell} to {'' if other_cell in cardinal_neighbours else 'NOT '}be a cardinal neighbour of {cell}"


def test_cell_is_diagonal_neighbour():
    cell = Cell(100, 100)

    diagonal_neighbours = {
        Cell(99, 99),
        Cell(101, 101),
        Cell(99, 101),
        Cell(101, 99),
    }

    for i in range(90, 111):
        for j in range(90, 111):
            other_cell = Cell(i, j)
            assert cell.is_neighbour(other_cell, 'diagonal') == (other_cell in diagonal_neighbours), \
                f"Expected {other_cell} to {'' if other_cell in diagonal_neighbours else 'NOT '}be a diagonal neighbour of {cell}"


def test_cell_is_any_neighbour():
    cell = Cell(100, 100)

    all_neighbours = {
        Cell(100, 99),
        Cell(100, 101),
        Cell(99, 100),
        Cell(101, 100),

        Cell(99, 99),
        Cell(101, 101),
        Cell(99, 101),
        Cell(101, 99),
    }

    for i in range(90, 111):
        for j in range(90, 111):
            other_cell = Cell(i, j)
            assert cell.is_neighbour(other_cell, 'all') == (other_cell in all_neighbours), \
                f"Expected {other_cell} to {'' if other_cell in all_neighbours else 'NOT '}be a neighbour of {cell}"
