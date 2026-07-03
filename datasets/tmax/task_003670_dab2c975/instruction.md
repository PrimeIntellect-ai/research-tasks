You are an engineer setting up a polyglot build system from scratch. Your task is to implement a C shared library that handles a binary schema migration, and then verify its ABI and logic using property-based testing in Python.

Specifically, you need to:

1. Create a C header file at `/home/user/migrate.h` that defines two structures and a function prototype:
   - `RecordV1`: contains an `int id` and a `char name[20]`.
   - `RecordV2`: contains an `int id`, a `char name[20]`, and a `float score`.
   - Function prototype: `void migrate_v1_to_v2(const struct RecordV1* in, struct RecordV2* out);`

2. Create a C source file at `/home/user/migrate.c` that implements `migrate_v1_to_v2`. The function should copy `id` and `name` exactly as they are from the input to the output, and initialize `score` to `0.0f`.

3. Compile the C code into a position-independent shared library named `/home/user/libmigrate.so`.

4. Create a Python script at `/home/user/test_migrate.py` that uses `ctypes` to interface with the shared library.
   - Use the `pytest` and `hypothesis` libraries to perform property-based testing. (You may need to install them using `pip`).
   - Use `hypothesis.strategies` to generate random integers for `id` and byte strings (length 0 to 19) for `name`.
   - The test function should initialize a V1 record, pass it to the C function along with an empty V2 record, and assert that `id` and `name` match the inputs, and `score` is exactly `0.0`.

5. Run your Python test script using `pytest` and redirect the output to `/home/user/test_result.log` (e.g., `python3 -m pytest /home/user/test_migrate.py > /home/user/test_result.log`).

Ensure all file paths are strictly followed and the test executes successfully.