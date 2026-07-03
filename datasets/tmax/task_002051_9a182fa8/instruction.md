You are a QA engineer setting up a test environment to verify a data schema migration script.

We have a Python script located at `/home/user/migrate.py` that migrates records from a v1 schema to a v2 schema. However, the current script contains a bug in its numerical calculations.

Your objectives:
1. Apply the patch file located at `/home/user/fix.patch` to `/home/user/migrate.py` to fix the bug.
2. Create a property-based test file at `/home/user/test_migration.py` using `pytest` and the `hypothesis` library to verify the correctness of the `migrate_v1_to_v2` function from `migrate.py`.
   - The test function must be named `test_migration_invariants`.
   - Use `hypothesis` to generate valid v1 records. A v1 record is a dictionary with:
     - `"id"`: an integer.
     - `"data"`: a list of floats. The floats should be constrained between -100.0 and 100.0, and the list must have a minimum size of 1 and a maximum size of 100.
   - Your test should pass the generated v1 dictionary to `migrate_v1_to_v2` and assert the following invariants on the returned v2 dictionary:
     a) `v2_data["record_id"]` must exactly equal `v1_data["id"]`.
     b) `v2_data["mean"]` must equal the arithmetic mean of `v1_data["data"]`. Because of floating-point arithmetic, you must use `math.isclose` with `rel_tol=1e-5` and `abs_tol=1e-8` for this assertion.
3. Run the test by executing `pytest /home/user/test_migration.py` and redirect the standard output to `/home/user/test_results.log`.

Make sure to leave `/home/user/test_results.log` on the filesystem.