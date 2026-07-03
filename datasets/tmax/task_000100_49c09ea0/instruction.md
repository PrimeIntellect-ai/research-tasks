I am an open-source maintainer, and I'm reviewing a pull request that tries to modernize our analytics backend. The PR author has left the project, and the pipeline is broken. I need you to step in, fix the code, and get the CI pipeline passing.

The project workspace is located at `/home/user/pr_review`.

Here is what you need to fix:
1. **Build Linking Error**: The C engine `math_engine.c` relies on the math library, but the `Makefile` is failing to link it properly, causing a failure when Python's `ctypes` tries to load the shared library. Fix the `Makefile`.
2. **C Memory Safety/Undefined Behavior**: The function `calculate_stddev` in `math_engine.c` contains a classic array bounds error (off-by-one) that causes undefined behavior/segfaults when computing the sum. Please find and fix this memory safety bug.
3. **Schema Migration**: The CI pipeline applies `schema_v1.sql` and then `schema_v2.sql` to a SQLite database. However, `schema_v2.sql` is currently empty. The Python test suite expects the `stats` table to have a `variance` column of type `REAL`. Write the correct SQL `ALTER TABLE` statement in `/home/user/pr_review/schema_v2.sql`.
4. **CI Pipeline Orchestration**: The script `/home/user/pr_review/run_ci.sh` orchestrates the build, DB setup, and testing. Ensure this script is fully executable and successfully completes.

Your goal is to modify the files in `/home/user/pr_review` so that running `./run_ci.sh` executes flawlessly.
If successful, the script will output a file named `/home/user/ci_success.log` containing the exact text `CI PASS`. 

Please inspect the directory, fix the bugs in the C code, Makefile, and SQL schema, and finally run `./run_ci.sh` to produce the required log file.