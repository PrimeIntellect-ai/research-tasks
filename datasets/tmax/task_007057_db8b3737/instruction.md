You are a utility script developer working on a high-performance Python package called `fastsum`. The package wraps a C-based algorithmic constraint solver that finds a subset of non-negative integers that sum up to a specific target.

The project is located at `/home/user/fastsum_project`.
However, the project is currently broken:
1. The `setup.py` file is misconfigured and fails to compile the C extension.
2. The package lacks proper testing to ensure the constraint solver behaves correctly.

Your task is to:
1. Navigate to `/home/user/fastsum_project`.
2. Identify and fix the build configuration error in `setup.py`.
3. Install the package into the current environment (e.g., using `pip install -e .`).
4. Write a property-based test script named `/home/user/test_fastsum.py` using the `hypothesis` and `pytest` libraries.
   - The test function must be named `test_subset_sum`.
   - Use `hypothesis` to generate random lists of non-negative integers (between 0 and 1000, max size 20) and a random target sum (between 0 and 10000).
   - The C extension function is `fastsum.solve(array, target)`. It returns a list of indices if a valid subset is found, or `None` if no subset exists.
   - Your test must verify the constraint: if the solver returns a list of indices, the sum of the elements in the input array at those indices must exactly equal the target. Also verify that all returned indices are unique and within the bounds of the array.
5. Run your test using `pytest /home/user/test_fastsum.py > /home/user/test_results.txt`.

Ensure that the final output file `/home/user/test_results.txt` contains the successful test execution results. You do not need to fix the C code; it is logically correct but the build orchestration and verification are missing.