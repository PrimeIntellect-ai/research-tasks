You are an engineer setting up a simple polyglot build system from scratch for a new project located in `/home/user/polyglot-eval`. 

This project consists of a concurrent expression evaluator written in Go (which uses goroutines and channels) and a structured data parsing utility written in Python. 

Currently, the project lacks a unified CI build script, and the Python test suite has a hidden flaw: it passes when you run individual test files locally, but fails when CI runs them all via test discovery due to an import ordering and global state mutation issue.

Your task is to:
1. Fix the Python testing issue. The tests are in `/home/user/polyglot-eval/tests/`. There are two test files: `test_a_parser.py` and `test_b_config.py`. They fail when run together via `python3 -m unittest discover -s tests` because of how a global configuration dictionary in `src/config.py` is imported and modified. Modify the Python code so that the tests pass regardless of execution order. Do NOT delete any test cases; fix the state isolation.
2. Create a bash script at `/home/user/polyglot-eval/build.sh`.
3. The script must read `/home/user/polyglot-eval/ci_config.json` using `jq`.
4. Extract the commands defined in the JSON file under the keys `"go_bench_cmd"` and `"py_test_cmd"`.
5. Execute the extracted Go benchmark command and then the Python test command sequentially.
6. Redirect the combined standard output and standard error of BOTH commands to `/home/user/build_out.log`.
7. Ensure the script is executable.

The `ci_config.json` file looks like this:
```json
{
  "go_bench_cmd": "cd go_src && go test -bench=.",
  "py_test_cmd": "PYTHONPATH=src python3 -m unittest discover -s tests"
}
```

Verify your work by running `./build.sh` and ensuring `/home/user/build_out.log` shows both the Go benchmark results and the Python tests passing successfully (OK).