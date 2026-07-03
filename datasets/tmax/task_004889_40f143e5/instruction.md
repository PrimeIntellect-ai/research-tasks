You are an integration developer tasked with testing a new mathematical API for a high-performance numerical service. We have vendored a fast C-based matrix library, but the provided build system is currently failing, and we need a Python interface to filter out problematic inputs before they reach the backend API.

Your tasks are:

1. **Fix the Vendored C Library**: 
   The C library is located at `/app/vendored/c_matrix_lib-1.0`. It contains a Makefile to build a shared library `libmatrix.so`. However, the build currently fails. Identify the issue in the Makefile and fix it so that `make` successfully produces `libmatrix.so`.

2. **Implement Python FFI**:
   Write a Python module at `/home/user/ffi_wrapper.py` that uses `ctypes` to load `/app/vendored/c_matrix_lib-1.0/libmatrix.so`. 
   The C library exposes the function:
   `double calculate_determinant(double* matrix, int n);`
   Wrap this function so it accepts a flat list of floats and an integer `n` (representing an $n \times n$ matrix) and returns the float determinant.

3. **Build the Input Sanitizer**:
   The API backend crashes when attempting to invert matrices that are singular or highly ill-conditioned. 
   Write a Python CLI tool at `/home/user/sanitizer.py` with the following usage:
   `python3 /home/user/sanitizer.py <input_directory> <output_results.json>`
   
   - `<input_directory>` will contain multiple JSON files. Each file has the format: `{"filename": "...", "n": 3, "data": [1.0, 2.5, ...]}` (where `data` is a flat list of length $n^2$).
   - For each file, compute the determinant using your `ffi_wrapper.py`.
   - If the absolute value of the determinant is strictly less than `1e-5`, the input must be rejected. Otherwise, it is accepted.
   - The tool must write a JSON dictionary to `<output_results.json>` mapping the base filename (e.g., `"matrix_1.json"`) to either `"reject"` or `"accept"`.

Ensure your sanitizer accurately classifies all inputs. Our automated test suite will run your script against an internal corpus of both clean and evil (ill-conditioned) matrices.