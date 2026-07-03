You are a Site Reliability Engineer responsible for deploying our new custom uptime monitoring utility, `miniping`. The source code for `miniping-1.2` has been vendored and extracted to `/app/miniping-1.2`. 

Your goal is to build, configure, and wrap this utility into an automated CI-like pipeline step. Complete the following objectives:

1. **Backup Strategy**: Before making any modifications, create a compressed tarball of the pristine vendored source directory. Save this backup exactly at `/home/user/miniping_backup.tar.gz`.

2. **Fix the Build**: The vendored `miniping-1.2` has a deliberate perturbation in its build configuration that prevents it from compiling. Identify and fix the issue in the C source or Makefile (hint: it fails to link a standard library required for its uptime heuristics). Compile the binary `miniping` inside the `/app/miniping-1.2` directory.

3. **Interactive Configuration Automation**: The `miniping` binary requires initial configuration by running `./miniping --init`. This is an interactive prompt that asks three questions:
   - "Set default timeout (ms):" 
   - "Set max retries:"
   - "Enable debug? (y/n):"
   Write an Expect script located exactly at `/home/user/setup_miniping.exp` that automates this process. The script must spawn the initialization command, answer "500" for the timeout, "3" for max retries, and "n" for debug mode, and then successfully exit.

4. **Monitoring Execution Wrapper**: Write a Bash script located exactly at `/home/user/run_uptime_check.sh`. This script must:
   - Take exactly one argument (a mock server response payload string).
   - Execute the compiled `miniping` binary (from `/app/miniping-1.2/miniping`) using the flag `--check` followed by the payload argument.
   - Print only the exact standard output produced by the `miniping` binary.

Your final wrapper script will be aggressively fuzzed and compared against a reference oracle to ensure absolute bit-exact equivalence of the output. Ensure all scripts are executable (`chmod +x`). Do not leave any hardcoded payloads in the wrapper script; it must dynamically pass the first argument to the binary.