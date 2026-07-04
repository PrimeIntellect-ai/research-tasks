You are an engineer setting up a lightweight, polyglot CI/CD pipeline from scratch. Your task is to write a Bash script that acts as the build runner for a custom build specification format called "PolyBuild".

Create a Bash script at `/home/user/ci_runner.sh` that takes exactly one argument: the absolute path to a PolyBuild (`.pb`) specification file.

The PolyBuild specification file contains line-oriented directives. Your script must parse the file and execute the pipeline according to the following rules, strictly in order:

**1. Checksum Verification**
Directives starting with `CHECKSUM <relative_filepath> <expected_sha256>`
* Calculate the SHA-256 hash of the specified file. (The filepath will be relative to the directory containing the `.pb` file).
* If the hash does not exactly match `<expected_sha256>`, your script must append the string `[ERROR] Checksum failed for <relative_filepath>` to `/home/user/build_output.log`, and immediately exit with status code `1`.

**2. Expression Parsing and Evaluation**
Directives starting with `EXPR <VAR_NAME> = <arithmetic_expression>`
* Parse and evaluate the arithmetic expression. The expression will only contain integers and the operators `+`, `-`, `*`, `/`, and `( )`. 
* You must evaluate this strictly as integer arithmetic.
* Write the result to `/home/user/build_env.sh` in the format: `export <VAR_NAME>=<evaluated_result>`.
* Ensure `/home/user/build_env.sh` is cleared or created fresh at the start of your script.

**3. Build Execution**
Directives starting with `BUILD <command>`
* Before running any build commands, your script must `source /home/user/build_env.sh` so that the evaluated variables are available in the environment.
* Execute the `<command>` from the directory containing the `.pb` file.
* If the command exits with a non-zero status code, your script must append `[ERROR] Build failed: <command>` to `/home/user/build_output.log`, and immediately exit with status code `2`.

**Completion**
* If all directives are processed successfully, your script must append `[SUCCESS] CI Pipeline Passed` to `/home/user/build_output.log` and exit with status code `0`.
* Your script must clear/overwrite `/home/user/build_output.log` at the very beginning of its execution.

**Test Setup**
To test your script, you can assume the following files exist (we will test your script against similar files):
* `/home/user/project/src/data.py`
* `/home/user/project/src/transform.rb`
* `/home/user/project/main.pb`

You must ensure your script `/home/user/ci_runner.sh` has executable permissions.