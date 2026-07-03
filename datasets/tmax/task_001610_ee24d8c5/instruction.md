I am working as a systems programmer and trying to bridge a C library with a Python test suite, but I am running into several linking and interfacing issues.

I have a project in `/home/user/project` that implements a constraint satisfaction checker in C. I want to test this logic using property-based testing in Python via the `hypothesis` library. 

Here are the files I currently have in `/home/user/project`:

1. `mathops.c`:
```c
#include <math.h>

// Constraint satisfaction: checks if point (x,y) satisfies the constraint of being strictly inside a circle of radius r
int is_inside_circle(double x, double y, double r) {
    double dist = sqrt(pow(x, 2) + pow(y, 2));
    return dist < r ? 1 : 0;
}
```

2. `Makefile`:
```makefile
libmathops.so: mathops.c
	gcc mathops.c -o libmathops.so
```

3. `test_mathops.py`:
```python
import ctypes
import os
from hypothesis import given, settings
from hypothesis.strategies import floats

lib_path = os.path.join(os.path.dirname(__file__), 'libmathops.so')
lib = ctypes.CDLL(lib_path)

# TODO: The ctypes argtypes and restype are missing, causing ABI issues during testing!

@given(x=floats(min_value=-100.0, max_value=100.0), y=floats(min_value=-100.0, max_value=100.0))
@settings(max_examples=500)
def test_circle_constraint(x, y):
    r = 150.0
    expected = 1 if (x**2 + y**2)**0.5 < r else 0
    
    # Call the C library
    result = lib.is_inside_circle(x, y, r)
    assert result == expected, f"Failed constraint: {x}, {y}. Expected {expected}, got {result}"

if __name__ == "__main__":
    test_circle_constraint()
    with open("/home/user/project/test_results.log", "w") as f:
        f.write("PASSED\n")
```

There are two major problems:
1. The `Makefile` is incorrect. It fails to build a proper shared library and fails to link the math library.
2. The Python script is missing the `ctypes` bindings (`argtypes` and `restype`), which causes type coercion errors and segmentation faults when hypothesis feeds random floats into the library.

Your task is to:
1. Fix the `Makefile` so it correctly builds a position-independent shared library (`libmathops.so`) and links the math library (`-lm`).
2. Fix `/home/user/project/test_mathops.py` to properly define the C-types for `is_inside_circle`.
3. Ensure `hypothesis` is installed (`pip install hypothesis` if needed).
4. Run `make` and then run the Python script to execute the property-based tests. 

If everything is correct, the script will create `/home/user/project/test_results.log` with the word `PASSED`.