#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <math.h>

#define RETURN_INCREF(obj)  \
    do {                    \
        Py_INCREF(obj);     \
        return obj;         \
    } while (0)

#define RETURN_INVALID_NEIGHBOUR                                                                    \
    PyErr_SetString(PyExc_ValueError, "neighbour_type must be 'cardinal', 'diagonal', or 'all'");   \
    return NULL;

static const int cardinal_offsets[4][2] = {{-1, 0}, {0, 1}, {1, 0}, {0, -1}};
static const int diagonal_offsets[4][2] = {{-1, -1}, {-1, 1}, {1, 1}, {1, -1}};
static const int all_offsets[8][2] = {{-1, -1}, {-1, 0}, {-1, 1}, {0, 1}, {1, 1}, {1, 0}, {1, -1}, {0, -1}};

static PyObject* cardinal_dirs = NULL;
static PyObject* diagonal_dirs = NULL;
static PyObject* all_dirs = NULL;

typedef struct {
    PyObject_HEAD
    int row;
    int column;
} CellObject;

// Initialisation and destruction
static PyObject* Cell_new(PyTypeObject* type, PyObject* args, PyObject* kwds);
static int Cell_init(CellObject* self, PyObject* args, PyObject* kwargs);

// Property methods
static PyObject* Cell_get_row(const CellObject* self, void* closure);
static PyObject* Cell_get_column(const CellObject* self, void* closure);
static PyObject* Cell_up(const CellObject* self, void* closure);
static PyObject* Cell_down(const CellObject* self, void* closure);
static PyObject* Cell_left(const CellObject* self, void* closure);
static PyObject* Cell_right(const CellObject* self, void* closure);

// Instance methods
static PyObject* Cell_neighbours(const CellObject* self, PyObject* neighbour_type);
static PyObject* Cell_is_neighbour(const CellObject* self, PyObject* args);
static PyObject* Cell_manhattan_distance(const CellObject* self, PyObject* other);
static PyObject* Cell_euclidean_distance(const CellObject* self, PyObject* other);
static PyObject* Cell_chebyshev_distance(const CellObject* self, PyObject* other);

// Static methods
static PyObject* Cell_neighbour_directions(PyObject* cls, PyObject* args);

// Operator methods
static PyObject* Cell_add(PyObject* self, PyObject* other);
static PyObject* Cell_sub(PyObject* self, PyObject* other);
static PyObject* Cell_richcompare(PyObject* self, PyObject* other, int op);

// Other dunder methods
static PyObject* Cell_to_complex(const CellObject* self);
static PyObject* Cell_iter(const CellObject* self);
static Py_hash_t Cell_hash(const CellObject* self);
static PyObject* Cell_repr(const CellObject* self);


static PyNumberMethods Cell_as_number = {
    .nb_add = Cell_add,
    .nb_subtract = Cell_sub,
};

static PyGetSetDef Cell_getset[] = {
    {"row", (getter)Cell_get_row, NULL, "Get the row coordinate of this cell.", NULL},
    {"column", (getter)Cell_get_column, NULL, "Get the column coordinate of this cell.", NULL},
    {"up", (getter)Cell_up, NULL, "Get the cell above this cell.", NULL},
    {"down", (getter)Cell_down, NULL, "Get the cell below this cell.", NULL},
    {"left", (getter)Cell_left, NULL, "Get the cell to the left of this cell.", NULL},
    {"right", (getter)Cell_right, NULL, "Get the cell to the right of this cell.", NULL},
    {NULL}  // Sentinel
};

static PyMethodDef Cell_methods[] = {
    {"neighbours", (PyCFunction) Cell_neighbours, METH_O, "Get the neighbours of the cell."},
    {"is_neighbour", (PyCFunction) Cell_is_neighbour, METH_VARARGS, "Check if the cell is a neighbour of another cell."},
    {"manhattan_distance", (PyCFunction) Cell_manhattan_distance, METH_O, "Calculate the Manhattan distance to another cell."},
    {"euclidean_distance", (PyCFunction) Cell_euclidean_distance, METH_O, "Calculate the Euclidean distance to another cell."},
    {"chebyshev_distance", (PyCFunction) Cell_chebyshev_distance, METH_O, "Calculate the Chebyshev distance to another cell."},
    {"neighbour_directions", (PyCFunction) Cell_neighbour_directions, METH_VARARGS | METH_STATIC, "Get the directions of the neighbours of the cell."},
    {"__complex__", (PyCFunction) Cell_to_complex, METH_NOARGS, "Convert the cell to a complex number."},
    {NULL}  // Sentinel
};

// Type definition
static PyTypeObject CellType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "cell.Cell",
    .tp_doc = "Represents a location in a 2-dimensional grid.",
    .tp_basicsize = sizeof(CellObject),
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_new = Cell_new,
    .tp_init = (initproc) Cell_init,
    .tp_as_number = &Cell_as_number,
    .tp_getset = Cell_getset,
    .tp_methods = Cell_methods,
    .tp_repr = (reprfunc) Cell_repr,
    .tp_richcompare = Cell_richcompare,
    .tp_iter = (getiterfunc) Cell_iter,
    .tp_hash = (hashfunc) Cell_hash,
};


static PyObject* create_cell(const int row, const int column) {
    CellObject* cell = PyObject_New(CellObject, &CellType);
    if (!cell) return PyErr_NoMemory();
    cell->row = row;
    cell->column = column;
    return (PyObject*) cell;
}

static PyObject* Cell_new(PyTypeObject* type, PyObject* args, PyObject* kwds) {
    CellObject* self = (CellObject*) type->tp_alloc(type, 0);
    if (self != NULL) {
        self->row = 0;
        self->column = 0;
    }
    return (PyObject*) self;
}

static int Cell_init(CellObject* self, PyObject* args, PyObject* kwargs) {
    static char* kwlist[] = {"row", "column", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "ii:Cell", kwlist, &self->row, &self->column)) {
        return -1;
    }
    return 0;
}

static PyObject* Cell_get_row(const CellObject* self, void* closure) {
    return PyLong_FromLong(self->row);
}

static PyObject* Cell_get_column(const CellObject* self, void* closure) {
    return PyLong_FromLong(self->column);
}

static PyObject* Cell_up(const CellObject* self, void* closure) {
    return create_cell(self->row - 1, self->column);
}

static PyObject* Cell_down(const CellObject* self, void* closure) {
    return create_cell(self->row + 1, self->column);
}

static PyObject* Cell_left(const CellObject* self, void* closure) {
    return create_cell(self->row, self->column - 1);
}

static PyObject* Cell_right(const CellObject* self, void* closure) {
    return create_cell(self->row, self->column + 1);
}

static PyObject* create_neighbours_tuple(const CellObject* self, const int neighbor_offsets[][2], const int size) {
    PyObject* neighbors_tuple = PyTuple_New(size);
    if (!neighbors_tuple) return PyErr_NoMemory();
    for (int i = 0; i < size; ++i) {
        const int nb_row = self->row + neighbor_offsets[i][0];
        const int nb_col = self->column + neighbor_offsets[i][1];
        PyTuple_SetItem(neighbors_tuple, i, create_cell(nb_row, nb_col));
    }
    return neighbors_tuple;
}

static PyObject* Cell_neighbours(const CellObject* self, PyObject* neighbour_type) {
    const char* neighbour_type_str;
    if (!PyArg_Parse(neighbour_type, "s:neighbours", &neighbour_type_str)) {
        return NULL;
    }

    if (strcmp(neighbour_type_str, "cardinal") == 0) return create_neighbours_tuple(self, cardinal_offsets, 4);
    if (strcmp(neighbour_type_str, "diagonal") == 0) return create_neighbours_tuple(self, diagonal_offsets, 4);
    if (strcmp(neighbour_type_str, "all") == 0) return create_neighbours_tuple(self, all_offsets, 8);

    RETURN_INVALID_NEIGHBOUR;
}

static PyObject* Cell_is_neighbour(const CellObject* self, PyObject* args) {
    CellObject* other;
    char* neighbour_type;
    if (!PyArg_ParseTuple(args, "O!s:is_neighbour", &CellType, &other, &neighbour_type)) return NULL;

    const int row_diff = abs(self->row - other->row);
    const int col_diff = abs(self->column - other->column);

    int is_nb;
    if (strcmp(neighbour_type, "cardinal") == 0) {
        is_nb = row_diff + col_diff == 1;
    } else if (strcmp(neighbour_type, "diagonal") == 0) {
        is_nb = row_diff == 1 && col_diff == 1;
    } else if (strcmp(neighbour_type, "all") == 0) {
        is_nb = row_diff == 1 && col_diff == 1 || row_diff + col_diff == 1;
    } else {
        RETURN_INVALID_NEIGHBOUR;
    }

    return PyBool_FromLong(is_nb);
}

static PyObject* Cell_manhattan_distance(const CellObject* self, PyObject* other) {
    const CellObject* other_cell;
    if (!PyArg_Parse(other, "O!:manhattan_distance", &CellType, &other_cell)) return NULL;
    const int a = abs(self->row - other_cell->row);
    const int b = abs(self->column - other_cell->column);
    return PyLong_FromLong(a + b);
}

static PyObject* Cell_euclidean_distance(const CellObject* self, PyObject* other) {
    const CellObject* other_cell;
    if (!PyArg_Parse(other, "O!:euclidean_distance", &CellType, &other_cell)) return NULL;
    const int a = self->row - other_cell->row;
    const int b = self->column - other_cell->column;
    return PyFloat_FromDouble(sqrt(a * a + b * b));
}

static PyObject* Cell_chebyshev_distance(const CellObject* self, PyObject* other) {
    const CellObject* other_cell;
    if (!PyArg_Parse(other, "O!:chebyshev_distance", &CellType, &other_cell)) return NULL;
    const int a = abs(self->row - other_cell->row);
    const int b = abs(self->column - other_cell->column);
    return PyLong_FromLong(a > b ? a : b);
}

static PyObject* Cell_neighbour_directions(PyObject* cls, PyObject* args) {
    char* neighbour_type_str;
    if (!PyArg_ParseTuple(args, "s:neighbour_directions", &neighbour_type_str)) return NULL;

    if (!cardinal_dirs) {
        cardinal_dirs = Py_BuildValue("((ii)(ii)(ii)(ii))", -1, 0, 0, 1, 1, 0, 0, -1);
        diagonal_dirs = Py_BuildValue("((ii)(ii)(ii)(ii))", -1, -1, -1, 1, 1, 1, 1, -1);
        all_dirs = Py_BuildValue("((ii)(ii)(ii)(ii)(ii)(ii)(ii)(ii))",
                                 -1, -1, -1, 0, -1, 1, 0, 1, 1, 1, 1, 0, 1, -1, 0, -1);

        if (!cardinal_dirs || !diagonal_dirs || !all_dirs) {
            Py_XDECREF(cardinal_dirs);
            Py_XDECREF(diagonal_dirs);
            Py_XDECREF(all_dirs);
            return PyErr_NoMemory();
        }
    }

    if (strcmp(neighbour_type_str, "cardinal") == 0) RETURN_INCREF(cardinal_dirs);
    if (strcmp(neighbour_type_str, "diagonal") == 0) RETURN_INCREF(diagonal_dirs);
    if (strcmp(neighbour_type_str, "all") == 0) RETURN_INCREF(all_dirs);

    RETURN_INVALID_NEIGHBOUR;
}

static PyObject* operate(PyObject* self, PyObject* other, int operation) {
    // When __radd__/__rsub__ is called, other is the Cell instead
    if (!PyObject_TypeCheck(self, &CellType)) {
        PyObject* temp = self;
        self = other;
        other = temp;
    }
    const CellObject* cell_self = (CellObject*) self;
    int other_row, other_col;

    if (PyComplex_Check(other) || PyLong_Check(other)) {
        const Py_complex complex_value = PyComplex_AsCComplex(other);
        other_row = (int) complex_value.real;
        other_col = (int) complex_value.imag;
    } else if (PyTuple_Check(other)) {
        if (!PyArg_ParseTuple(other, "ii;expected tuple to have exactly 2 elements", &other_row, &other_col)) {
            return NULL;
        }
    } else if (PyObject_TypeCheck(other, &CellType)) {
        const CellObject* other_cell = (CellObject*) other;
        other_row = other_cell->row;
        other_col = other_cell->column;
    } else {
        Py_RETURN_NOTIMPLEMENTED;
    }

    int new_row, new_col;

    switch (operation) {
        case Py_nb_add:
            new_row = cell_self->row + other_row;
            new_col = cell_self->column + other_col;
            break;
        case Py_nb_subtract:
            new_row = cell_self->row - other_row;
            new_col = cell_self->column - other_col;
            break;
        default:
            Py_RETURN_NOTIMPLEMENTED;
    }

    return create_cell(new_row, new_col);
}

static PyObject* Cell_add(PyObject* self, PyObject* other) {
    return operate(self, other, Py_nb_add);
}

static PyObject* Cell_sub(PyObject* self, PyObject* other) {
    return operate(self, other, Py_nb_subtract);
}

static PyObject* Cell_richcompare(PyObject* self, PyObject* other, const int op) {
    if (!PyObject_TypeCheck(other, &CellType)) {
        Py_RETURN_NOTIMPLEMENTED;
    }
    const CellObject* cell1 = (CellObject*) self;
    const CellObject* cell2 = (CellObject*) other;
    int result;

    switch (op) {
        case Py_EQ:
            result = cell1->row == cell2->row && cell1->column == cell2->column;
            break;
        case Py_NE:
            result = cell1->row != cell2->row || cell1->column != cell2->column;
            break;
        default:
            Py_RETURN_NOTIMPLEMENTED;
    }

    return PyBool_FromLong(result);
}

static PyObject* Cell_to_complex(const CellObject* self) {
    return PyComplex_FromCComplex((Py_complex){self->row, self->column});
}

static PyObject* Cell_iter(const CellObject* self) {
    PyObject* tuple = PyTuple_Pack(2, PyLong_FromLong(self->row), PyLong_FromLong(self->column));
    if (!tuple) return NULL;
    return PyObject_GetIter(tuple);
}

/*
 * The following hashing code is based on the tuple hashing algorithm from CPython's source code.
 * It has been modified to suit the needs of hashing two integers (`row` and `column` in the `CellObject` struct).
 * This allows objects of type `CellObject` to produce the same hash as their equivalent tuple.
 * The original tuple hashing can be found in CPython's GitHub repository at https://github.com/python/cpython,
 * and the relevant code is located in the `Objects/tupleobject.c` file.
 *
 * Permalink to the `tuple_hash` function:
 * https://github.com/python/cpython/blob/2228e92da31ca7344a163498f848973a1b356597/Objects/tupleobject.c#L318
 */

#if SIZEOF_PY_UHASH_T > 4
#define HASH_XXPRIME_1 ((Py_uhash_t)11400714785074694791ULL)
#define HASH_XXPRIME_2 ((Py_uhash_t)14029467366897019727ULL)
#define HASH_XXPRIME_5 ((Py_uhash_t)2870177450012600261ULL)
#define HASH_XXROTATE(x) ((x << 31) | (x >> 33))  /* Rotate left 31 bits */
#else
#define HASH_XXPRIME_1 ((Py_uhash_t)2654435761UL)
#define HASH_XXPRIME_2 ((Py_uhash_t)2246822519UL)
#define HASH_XXPRIME_5 ((Py_uhash_t)374761393UL)
#define HASH_XXROTATE(x) ((x << 13) | (x >> 19))  /* Rotate left 13 bits */
#endif

static int hash_int(Py_uhash_t* acc, const int number) {
    const Py_uhash_t hash = PyObject_Hash(PyLong_FromLong(number));
    if (hash == (Py_uhash_t) -1) {
        return 1;
    }
    *acc = HASH_XXROTATE(*acc + hash * HASH_XXPRIME_2) * HASH_XXPRIME_1;
    return 0;
}

static Py_hash_t Cell_hash(const CellObject* self) {
    Py_uhash_t acc = HASH_XXPRIME_5;

    if (hash_int(&acc, self->row)) return -1;
    if (hash_int(&acc, self->column)) return -1;

    acc += 2 ^ (HASH_XXPRIME_5 ^ 3527539UL);

    if (acc == (Py_uhash_t) -1) {
        return 1546275796;
    }

    return acc;
}

static PyObject* Cell_repr(const CellObject* self) {
    return PyUnicode_FromFormat("Cell(row=%d, column=%d)", self->row, self->column);
}

// Module definition
static PyModuleDef cellmodule = {
    PyModuleDef_HEAD_INIT,
    .m_name = "cell",
    .m_doc = "Module containing the Cell class.",
    .m_size = -1,
    .m_methods = NULL,
    .m_slots = NULL,
    .m_traverse = NULL,
    .m_clear = NULL,
    .m_free = NULL,
};

// Module initialization
PyMODINIT_FUNC PyInit_cell(void) {
    if (PyType_Ready(&CellType) < 0) {
        return NULL;
    }
    PyObject* m = PyModule_Create(&cellmodule);
    if (m == NULL) {
        return NULL;
    }
    Py_INCREF(&CellType);
    if (PyModule_AddObject(m, "Cell", (PyObject*) &CellType) < 0) {
        Py_DECREF(&CellType);
        Py_DECREF(m);
        return NULL;
    }
    return m;
}
