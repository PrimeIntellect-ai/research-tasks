You are a platform engineer maintaining a local CI/CD pipeline for a legacy data processing microservice.

We have a C program located at `/home/user/src/parser.c` that deserializes a custom key-value configuration file. The program currently has a memory leak. 

Your task involves two parts:

1. **Fix the memory leak**: Analyze `/home/user/src/parser.c` and fix the memory leak. The program must compile without warnings using `gcc` and execute with 0 memory leaks when run under `valgrind`.

2. **Set up the CI script**: Create an executable Bash script at `/home/user/run_ci.sh` that simulates a CI pipeline. The script must perform the following steps in order:
   - Read the semantic version string from `/home/user/version.txt`.
   - Perform a semantic version comparison to ensure the version is greater than or equal to `2.0.0`. If it is strictly less than `2.0.0`, the script must exit immediately with status code `1`.
   - Compile `/home/user/src/parser.c` to an executable named `/home/user/parser` using `gcc`.
   - Run the compiled program against the sample data file at `/home/user/data.txt` using `valgrind` with the flags `--leak-check=full` and `--error-exitcode=1`.
   - If the program runs successfully and Valgrind detects no memory leaks, the script must write a final success log to `/home/user/ci_report.txt` containing exactly: `CI SUCCESS: <version>` (where `<version>` is the exact string read from `version.txt`).

**Constraints and Notes:**
- You may use standard Unix utilities (like `sort -V`, `awk`, etc.) in your bash script for the semantic version comparison.
- Make sure `/home/user/run_ci.sh` is given execute permissions.
- Do not modify `/home/user/data.txt` or `/home/user/version.txt`.