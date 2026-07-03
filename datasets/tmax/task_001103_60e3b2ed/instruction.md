You are a systems programmer debugging a C library linking issue and setting up an automated testing pipeline.

In `/home/user/project/src`, there are two C source files: `hw_mock.c` and `metrics.c`. 
Currently, `metrics.c` is failing to compile and link properly because it requires specific conditional build flags and depends on symbols from `hw_mock.c`.

Your tasks:

1. **Structured Data Parsing & Conditional Build**:
   Read `/home/user/project/build_config.json`. Extract the required C compiler flags from the `"cflags"` array.
   Compile `hw_mock.c` into a shared library named `libhwmock.so`.
   Compile `metrics.c` into a shared library named `libmetrics.so`. Ensure that `libmetrics.so` uses the compiler flags from the JSON file and is properly dynamically linked against `libhwmock.so` (it uses the `hw_init` function). Both libraries should be placed in `/home/user/project/lib`.

2. **Schema Migration**:
   There is an existing SQLite database at `/home/user/project/db/metrics.db` with a table `results(id INTEGER PRIMARY KEY, metric_name TEXT, metric_value REAL)`.
   Perform a schema migration to add a new column named `status` of type `TEXT` to the `results` table.

3. **Integration Testing via Python**:
   Write a Python script at `/home/user/project/test_metrics.py`. This script must:
   - Use the `ctypes` library to load `/home/user/project/lib/libmetrics.so`. (You may need to handle `LD_LIBRARY_PATH` or use absolute paths).
   - Define the correct signature for the C function `double get_system_score()`.
   - Call `get_system_score()`.
   - Connect to `/home/user/project/db/metrics.db` and insert a new row into the `results` table with:
     - `metric_name`: `"sys_score"`
     - `metric_value`: the exact double returned by the C function.
     - `status`: `"PASS"`

4. **Output Verification**:
   Finally, your Python script (or a separate script) must query all rows from the `results` table, order them by `id` ascending, and export the entire table as a JSON array of objects to `/home/user/output.json`. 
   Each object should have the keys: `"id"`, `"metric_name"`, `"metric_value"`, and `"status"`.

All files must be created or modified within the `/home/user/project` directory structure.