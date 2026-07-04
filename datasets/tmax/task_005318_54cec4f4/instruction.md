You are a mobile build engineer maintaining the CI telemetry pipeline. Your team uses a highly optimized C library to extract metrics from raw build logs, and a Go service to process and store these metrics. 

However, a recent system update broke the build pipeline. The C library no longer compiles correctly as a shared object, the Go telemetry processor is missing, and the database schema is out of date.

Your task is to fix the pipeline by completing the following steps:

1. **Repair the C Compilation**:
   Navigate to `/home/user/telemetry/`. You will find `telemetry.c`, `telemetry.h`, and a `Makefile`. The `Makefile` is broken and fails to produce a valid shared library. Fix the `Makefile` so that running `make` correctly compiles `telemetry.c` into a shared library named `libtelemetry.so`. (Hint: Ensure position-independent code and shared object flags are used).

2. **Schema Migration**:
   There is an SQLite database at `/home/user/metrics.db` with a table named `builds`. The current schema is:
   `CREATE TABLE builds (id INTEGER PRIMARY KEY, device TEXT, build_time REAL);`
   The new telemetry format requires two new columns. Perform a schema migration to add:
   - `memory_used` (INTEGER)
   - `battery_drain` (REAL)

3. **Write the Go Telemetry Processor**:
   Write a Go program at `/home/user/telemetry/process.go` that does the following:
   - Uses `cgo` to link against `libtelemetry.so` in the same directory.
   - Calls the C function `int process_telemetry(const char* input_file, char* output_buffer, int max_len);` defined in `telemetry.h`.
   - Pass `/home/user/telemetry/raw.dat` as the input file path, and provide a sufficiently large buffer (e.g., 1024 bytes) to receive the output.
   - The C function will populate the buffer with a JSON string and return `0` on success.
   - Parse the JSON string. It will have the keys: `device`, `build_time`, `memory_used`, and `battery_drain`.
   - Insert this parsed data as a new row into the `builds` table in the SQLite database at `/home/user/metrics.db`.
   
4. **Execute**:
   Run your Go program (e.g., `LD_LIBRARY_PATH=/home/user/telemetry go run process.go`) so that the database is updated with the new telemetry data.