You are a script developer working on a mathematical utility for processing large polynomial datasets. We have a C library that efficiently sorts and merges polynomial terms, but you need to compile it and write a Python wrapper to perform a differential analysis between two datasets.

You have been provided with the following files in `/home/user/`:
- `math_utils.c`: Contains the C logic for sorting and merging polynomial terms.
- `poly_A.txt`: Dataset representing Polynomial A. Each line is `coefficient,exponent` (integers).
- `poly_B.txt`: Dataset representing Polynomial B. Each line is `coefficient,exponent` (integers).

Perform the following tasks:

1. **Compile the Shared Library (Conditional Build):**
   Compile `math_utils.c` into a shared library named `/home/user/libpoly.so`. 
   You must compile it with position-independent code (`-fPIC`) and as a shared object. 
   **Important:** The C code contains conditional compilation directives. You must define the macro `CONDENSE_ZERO` during compilation (e.g., using `-D`) so that the C function automatically removes terms with a coefficient of `0` during its merge phase.

2. **Write the Python Wrapper (`/home/user/poly_diff.py`):**
   Write a Python script that uses the `ctypes` module to interface with `/home/user/libpoly.so`.
   - You must design a custom `ctypes.Structure` named `PolyTerm` that matches the ABI of the C struct exactly. The C struct is defined as:
     ```c
     struct PolyTerm {
         int coeff;
         int exp;
     };
     ```
   - The C function has the signature: 
     `void sort_and_merge(struct PolyTerm* terms, int* n_terms);`
   - Your script should parse `poly_A.txt` and `poly_B.txt`, converting them into arrays of your custom `PolyTerm` structures.
   - Use the C library's `sort_and_merge` function to simplify both Polynomial A and Polynomial B.
   - After simplification, compute the mathematical difference: `Polynomial A - Polynomial B`. (Subtract the coefficients of matching exponents. If an exponent is present in one polynomial but not the other, treat the missing coefficient as 0).
   - Filter out any resulting terms that have a coefficient of `0`.
   - Sort the resulting polynomial terms by exponent in strictly descending order.

3. **Output the Result:**
   Your Python script must write the final diffed polynomial to `/home/user/poly_diff_result.txt`.
   The file should contain one term per line in the format `coefficient,exponent`.

Ensure your Python script is fully self-contained, executes successfully, and accurately produces the result file.