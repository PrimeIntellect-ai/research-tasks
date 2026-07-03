You are tasked with porting a legacy data processing tool to run in a minimal container environment. The container lacks a standard C library, so you must implement a critical processing function in raw assembly and integrate it with the existing Python tool via Foreign Function Interface (FFI). Additionally, the legacy database schema must be updated to store the new processed values.

Your workspace is in `/home/user`.

Here is the current system state:
- A SQLite database exists at `/home/user/legacy/db.sqlite` with a table `metrics` containing the columns: `id INTEGER` and `raw_val INTEGER`. 
- A Python script `/home/user/legacy/processor.py` exists, which reads `raw_val` from the database, passes it to a C shared library (`libcustom.so`) via `ctypes`, and attempts to save the result back into a column named `hash_val`.

Your task is to complete the porting process by fulfilling the following requirements:

1. **Schema Migration:** Write a Bash script `/home/user/migrate.sh` that updates `/home/user/legacy/db.sqlite`. It must add the `hash_val INTEGER` column to the `metrics` table.

2. **Assembly-level Minimal Program:** The original `libcustom.so` was lost. Write raw x86_64 assembly (GNU syntax) in `/home/user/custom.s`. It must export a global function `compute_hash` that takes a single 32-bit integer (following the System V AMD64 ABI), XORs it with `0x5A`, adds `12` to the result, and returns it.

3. **Build and Execute:** Write a main Bash script `/home/user/build_and_run.sh` that performs the following steps in order:
   - Compiles `/home/user/custom.s` into a shared library `/home/user/legacy/libcustom.so` without linking the standard C library (`-nostdlib`, `-fPIC`, `-shared`).
   - Executes `/home/user/migrate.sh`.
   - Executes `/home/user/legacy/processor.py`.
   - Dumps the final contents of the `metrics` table (all columns) to `/home/user/final_dump.txt` using the command `sqlite3 /home/user/legacy/db.sqlite "SELECT * FROM metrics;" > /home/user/final_dump.txt`.

Ensure your Bash scripts are executable (you may need to `chmod +x`). Once you are done, run `/home/user/build_and_run.sh` so that `/home/user/final_dump.txt` is generated.