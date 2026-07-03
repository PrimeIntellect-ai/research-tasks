I am a researcher running statistical simulations and parameter estimation over large datasets. I have a data processing pipeline that produces `.npz` files containing multi-dimensional arrays. Each file contains three arrays: `x`, `a`, and `b` (all of the same shape). 

In a valid ("clean") simulation result, every element must satisfy the nonlinear equation:
$x^3 + a \cdot x + b = 0$
within a numerical tolerance of `1e-4`. Furthermore, a valid result must not contain any `NaN` or `Infinity` values. 
Sometimes my simulation diverges or gets corrupted, producing "evil" files where the condition is violated for at least one element, or numerical instabilities (NaN/Inf) are present.

I need your help with two things:

1. **Fix my local solver package**: I have a vendored package located at `/app/root_finder_pkg` which I use to generate these simulations. However, it currently fails to install because I messed up the `setup.py` file recently. Please fix the package and install it in the local Python environment.
2. **Create a sanitizer**: Write a Python script at `/home/user/sanitizer.py` that takes a single file path as a command-line argument. The script must load the `.npz` file, perform multi-dimensional array manipulation to check if the arrays represent a clean or evil simulation, and exit with status code `0` if the file is strictly "clean", and `1` if the file is "evil".

Your sanitizer will be tested against two corpora of simulation results to ensure it completely separates the valid runs from the corrupted ones. Ensure your code is efficient as the arrays can be large.

Please write `/home/user/sanitizer.py` and fix the package at `/app/root_finder_pkg`.