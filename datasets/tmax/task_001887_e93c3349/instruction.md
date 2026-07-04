You are tasked with debugging a failing CI build and implementing a security linter for our test suite. 

Our CI pipeline relies on a locally vendored version of the `bats-core` testing framework. Recently, an unauthorized modification or bad merge corrupted the vendored framework. Whenever we try to run any valid test file, the test runner fails mysteriously, usually failing to source the test file or crashing with an intermediate variable error.

**Part 1: Fix the Vendored Package**
1. The `bats-core` package is vendored at `/app/bats-core-1.11.0`.
2. Use intermediate state tracing and debugging to identify why the test runner is failing to execute valid test files. 
3. Fix the deliberate perturbation within its `libexec/bats-core` scripts. Once fixed, running `/app/bats-core-1.11.0/bin/bats <valid_test_file>` should work perfectly.

**Part 2: Implement a Bats Linter (Adversarial Filter)**
Our developers keep committing tests that contain dangerous commands or malformed headers. You must write a robust Bash script at `/home/user/bats_linter.sh` that takes a single file path as its argument and validates the script.

The linter must enforce the following rules:
1. **Shebang Rule:** The very first line of the file MUST be exactly `#!/usr/bin/env bats`.
2. **Forbidden Keyword Rule:** The file MUST NOT contain the exact word `eval` anywhere in the file (as a command, within comments, or inside strings; matching the regex `\beval\b`).
3. **Behavior:** The script must output nothing to stdout/stderr (or purely diagnostic info, it doesn't matter) but MUST return an **exit code of 0** if the file is clean, and an **exit code of 1** if the file violates any of the rules.

To help you develop and minimize your tests (using delta debugging principles), we have provided two directories:
* `/app/corpus/clean/`: Contains perfectly valid `.bats` files.
* `/app/corpus/evil/`: Contains malformed or dangerous `.bats` files.

Your script at `/home/user/bats_linter.sh` will be evaluated against a hidden, much larger test suite containing adversarial inputs designed to trick naive grep/awk statements. Ensure your Bash script is rigorous.