You have inherited a C-based data processing tool from a developer who abruptly left the company. The tool, `time_series_filter`, is designed to parse JSON payloads containing arrays of high-precision timestamp data (Unix epoch with microsecond resolution), validate the progression of time, and output the normalized values.

The tool relies on a vendored version of the `cJSON` library located at `/app/cJSON-1.7.15`. However, the environment is currently broken:
1. The previous developer mentioned they accidentally deleted a critical source file in the vendored `cJSON` directory right before they left, though they usually kept backups in hidden directories on the filesystem.
2. The Makefile for the vendored `cJSON` library is failing with linker errors when trying to build the shared object.
3. Even when the build is hacked together, `time_series_filter.c` (located in `/home/user/`) crashes on intermediate validation assertions. The developer noted: "There's a subtle bug where our microsecond timestamps are losing precision and failing the strict monotonicity assertions, but I haven't tracked down why."

Your tasks:
1. Locate and recover the deleted file necessary to build the vendored `cJSON` package.
2. Diagnose and fix the linker errors in `/app/cJSON-1.7.15/Makefile` so that `make` successfully builds `libcjson.so`.
3. Inspect `/home/user/time_series_filter.c` and fix the floating-point precision bug that causes the timestamps to lose microsecond accuracy and fail the assertions. 
4. Compile your fixed `time_series_filter.c` against the built `libcjson.so` and output the final executable to `/home/user/time_series_filter`.

The final program must accept a single JSON string as its first command-line argument (`argv[1]`), parse the array of numbers, and print each number on a new line formatted to exactly six decimal places (e.g., `1609459200.123456`). Do not print any extraneous text.

Ensure your compiled executable is located precisely at `/home/user/time_series_filter`.