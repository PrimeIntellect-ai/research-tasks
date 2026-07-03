You are an open-source maintainer reviewing a broken Pull Request (PR) submitted to your numerical computation library. The PR attempts to introduce a custom data structure for sparse polynomials (`SparsePolynomial`) and implement basic arithmetic, specifically multiplication. However, the continuous integration (CI) pipeline is failing because the numerical algorithm for multiplication is fundamentally flawed, and the contributor didn't provide proper tests or an orchestration script.

Your task is to fix the PR, write the missing tests, and set up an end-to-end test orchestration script.

**Step 1: Fix the `SparsePolynomial` implementation**
The source code is located at `/home/user/sparse_poly_pr/sparse_poly.py`.
The `__mul__` method has critical bugs related to numerical algorithm implementation. Fix it so that:
1. It correctly multiplies two polynomials (accumulating products of coefficients for added degrees).
2. It correctly removes any terms that end up with a coefficient of exactly `0` (this should be handled by the existing `_cleanup` method, but ensure the logic works).

**Step 2: Write the test suite**
Create a test file at `/home/user/sparse_poly_pr/test_sparse_poly.py` using `pytest`. You must implement exactly these three test functions:
1. `test_mult_basic`: Verify that `(2x^2 + 3) * (x + 4)` equals `2x^3 + 8x^2 + 3x + 12`.
2. `test_mult_zero_cancellation`: Verify that `(x + 1) * (x - 1)` equals `x^2 - 1`. Assert explicitly that the degree `1` term is *not* present in the `coeffs` dictionary at all.
3. `test_mult_large_sparse`: Verify that `(5x^100) * (2x^50 + 3)` equals `10x^150 + 15x^100`.

*Note: The `SparsePolynomial` constructor takes a dictionary of `{degree: coefficient}`.*

**Step 3: End-to-end test orchestration**
Create a bash script at `/home/user/sparse_poly_pr/run_tests.sh` that:
1. Installs `pytest` and `pytest-json-report` using pip.
2. Runs the test suite `test_sparse_poly.py`.
3. Generates a JSON test report and saves it exactly to `/home/user/sparse_poly_pr/test_report.json`.

Ensure the script has executable permissions (`chmod +x`). Execute your script to verify that all tests pass and the report is generated correctly.