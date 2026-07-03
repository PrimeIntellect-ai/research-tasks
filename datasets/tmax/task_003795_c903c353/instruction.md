You are a performance and testing engineer tasked with debugging a critical Bash-based data query engine that is failing intermittently in production. 

The query engine is located at `/home/user/query_engine`.
It consists of a main entry point `/home/user/query_engine/query.sh` and a data file `/home/user/query_engine/db.txt`.

Currently, the engine has several serious issues:
1. **Dependency Conflict:** `query.sh` sources a local library that inadvertently overrides standard shell utilities, causing unpredictable behavior and slow execution.
2. **Crash/Performance Bug:** The script crashes or hangs when provided with certain special characters due to unsafe query evaluation.
3. **Incorrect Query Results:** For complex queries, it occasionally returns corrupted output lines.

Your task is to fix the engine and establish a robust testing pipeline.

**Requirements:**

1. **Fix the Dependency Conflict:** Modify `/home/user/query_engine/query.sh` so it uses standard system utilities instead of the broken local overrides, without removing the necessary functions it relies on.
2. **Fuzz Testing:** Create a script at `/home/user/query_engine/fuzz.sh` that generates random strings containing standard alphanumeric characters and special shell characters (e.g., `*`, `[`, `"`, `'`, `\`, `?`). The script should feed these into `./query.sh "$fuzzed_string"`. Use this fuzzer to identify the inputs that break the script.
3. **Fix the Query Engine:** Modify `/home/user/query_engine/query.sh` to properly escape and handle all inputs safely so it no longer hangs or crashes, and correctly searches `db.txt` using `grep -E`.
4. **Regression Test Suite:** Create a script at `/home/user/query_engine/regression_test.sh` that runs `query.sh` against at least three specific test cases:
   - A normal query (e.g., `"STATUS=200"`)
   - A query with special characters (e.g., `"ERROR=50*[^a-z]"`)
   - An empty query string
   The test script must exit with code 0 if all tests pass (i.e., return the expected filtered rows without crashing) and exit with code 1 if any fail.
5. **Final Validation:** Run the fixed engine with the query string `USER="admin" OR STATUS=500` and save the exact standard output to `/home/user/query_engine/final_output.log`.

All scripts must be executable. Use only Bash built-ins, coreutils, and standard CLI tools.