You are an integration developer working on a lightweight API routing module written in C. The project currently has a broken build configuration, and we need to orchestrate an end-to-end test suite using Bash to verify its URL routing capabilities.

Here is the current state of your workspace in `/home/user/api_project/`:
1. `router.c`: A C program that takes a single URL path as a command-line argument, parses the route and query parameters, and prints them to standard output. If the URL is invalid (doesn't start with `/`), it exits with code 1.
2. `Makefile`: A broken Makefile that fails to compile the `router` executable.
3. `urls.txt`: A file containing a list of test URLs, one per line.

Your tasks are:

**Step 1: Fix the Build System**
Repair the `/home/user/api_project/Makefile` so that running `make` in the `/home/user/api_project/` directory successfully compiles `router.c` into an executable named `router`. (Note: The C code itself is perfectly fine; only the Makefile is broken).

**Step 2: Orchestrate the Tests**
Write a Bash script at `/home/user/api_project/run_tests.sh`. This script must:
1. Ensure it is executable.
2. Read the URLs from `/home/user/api_project/urls.txt` line by line.
3. Execute the compiled `./router` program for each URL.
4. Capture the standard output and exit code of the router.
5. Generate a test report file exactly at `/home/user/api_project/test_report.log`.

**Report Format Requirements:**
For each URL tested, append exactly one line to `test_report.log`.
- If the router succeeds (exit code 0), the line must be formatted exactly as:
  `SUCCESS - <original_url> -> <output_of_router_concatenated_with_spaces>`
  *(Note: The router outputs "Route: [route]" and "Params: [params]" on separate lines. Your Bash script must replace the newline between them with a single space so it fits on one line).*
- If the router fails (exit code non-zero), the line must be formatted exactly as:
  `FAILURE - <original_url> -> INVALID_ROUTE`

Example of expected lines in `test_report.log`:
`SUCCESS - /api/users?id=10 -> Route: /api/users Params: id=10`
`FAILURE - api/login -> INVALID_ROUTE`

Run your `run_tests.sh` script to generate the final `test_report.log`.