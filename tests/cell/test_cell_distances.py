import pytest
from utils_anviks import Cell


@pytest.mark.parametrize(
    ('offset_row', 'offset_col'),
    [
        pytest.param(-2, 0, id='N'),
        pytest.param(-1, -1, id='NW'),
        pytest.param(0, -2, id='W'),
        pytest.param(1, -1, id='SW'),
        pytest.param(2, 0, id='S'),
        pytest.param(1, 1, id='SE'),
        pytest.param(0, 2, id='E'),
        pytest.param(-1, 1, id='NE'),
    ])
def test_manhattan_distance(offset_row: int, offset_col: int):
    cell = Cell(0, 0)
    assert cell.manhattan_distance(Cell(offset_row, offset_col)) == 2


@pytest.mark.parametrize(
    ('row', 'column', 'expected'),
    [
        pytest.param(0, 0, 0, id='same_cell'),
        pytest.param(1, 1, 1.4142135623730951, id='diagonal_distance'),
        pytest.param(2, 2, 2.8284271247461903, id='further_diagonal_distance'),
        pytest.param(1, 0, 1.0, id='horizontal_distance'),
        pytest.param(0, 1, 1.0, id='vertical_distance'),
    ])
def test_euclidean_distance(row: int, column: int, expected: float):
    cell = Cell(0, 0)
    assert cell.euclidean_distance(Cell(row, column)) == expected, \
        f'Expected {expected} but got {cell.euclidean_distance(Cell(row, column))}'


@pytest.mark.parametrize(
    ('offset_row', 'offset_col', 'expected'),
    [
        pytest.param(-2, 0, 2, id='N'),
        pytest.param(-1, -1, 1, id='NW'),
        pytest.param(0, -2, 2, id='W'),
        pytest.param(1, -1, 1, id='SW'),
        pytest.param(2, 0, 2, id='S'),
        pytest.param(1, 1, 1, id='SE'),
        pytest.param(0, 2, 2, id='E'),
        pytest.param(-1, 1, 1, id='NE'),
    ])
def test_chebyshev_distance(offset_row: int, offset_col: int, expected: int):
    cell = Cell(0, 0)
    assert cell.chebyshev_distance(Cell(offset_row, offset_col)) == expected, \
        f'Expected {expected} but got {cell.chebyshev_distance(Cell(offset_row, offset_col))}'
