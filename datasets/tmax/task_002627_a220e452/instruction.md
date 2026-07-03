You are a QA engineer tasked with setting up a concurrent test environment for a custom mathematical interpreter written in Bash. The test suite currently passes locally for some developers but fails in CI due to file globbing issues when evaluating multiplication, and the tests are running too slowly because they execute sequentially.

Your goal is to patch the interpreter, migrate the old test fixtures into a new file-per-test format, and write a test runner that executes the tests concurrently using Bash background jobs.

Here are the requirements:

1. **Patch the Interpreter:**
   - The interpreter script is located at `/home/user/interpreter.sh`.
   - A patch file that fixes a globbing bug (which causes `*` to expand to filenames) is provided at `/home/user/fix_globbing.patch`.
   - Apply this patch to `/home/user/interpreter.sh`.

2. **Schema Migration (Test Fixture Setup):**
   - The old test fixtures are stored in a CSV file at `/home/user/fixtures.csv` in the format `test_id,rpn_expression`.
   - Write a script named `/home/user/test_runner.sh`.
   - The script must first create a directory `/home/user/test_data/`.
   - It must read `/home/user/fixtures.csv` and create an individual text file for each test case inside `/home/user/test_data/`. The file must be named `test_<id>.txt` and contain exactly the `rpn_expression` string (no trailing newlines are required, but ensure the expression is correct).

3. **Concurrent Test Execution:**
   - After migrating the fixtures, your `/home/user/test_runner.sh` script must execute `/home/user/interpreter.sh` for each fixture file.
   - You must pass the expression to the interpreter as a single string argument (e.g., `./interpreter.sh "$(cat test_data/test_1.txt)"`).
   - The executions **must** be spawned concurrently as background jobs using `&` and synchronized using `wait`.

4. **Result Collation:**
   - The script must collect the standard output of each interpreter run.
   - It must generate a final report at `/home/user/test_report.log`.
   - The report must contain exactly one line per test in the format: `Test <id>: <result>`.
   - The report must be numerically sorted by the test ID.

Ensure your `test_runner.sh` script is executable and run it to produce the final `test_report.log` and populate the `test_data` directory.