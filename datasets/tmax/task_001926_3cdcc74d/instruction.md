You are tasked with debugging a data processing repository that has suffered multiple regressions over the last 200 commits. 

The repository is located at `/home/user/data_processor`. It contains:
- `process_logs.sh`: A Bash script that processes log files.
- `parse_time.c`: A C helper program used by the data processing pipeline.
- `Makefile`: Builds the `parse_time` binary.
- `test_input.log`: A sample log file.

Currently, if you run `make` at `HEAD`, it fails to compile due to a linker error.

Furthermore, there is a logic regression. At some point in the past, a timezone/filtering bug was introduced into `process_logs.sh`, causing it to output an incorrect event count for `test_input.log`. We know that commit `HEAD~195` is a "good" commit where both the compilation succeeds and the logic produces the correct count. The current `HEAD` is "bad" (has the logic bug, and also doesn't compile).

Your tasks:
1. Figure out the compiler/linker error in the current `HEAD`.
2. Find the *exact commit* that introduced the data processing logic bug in `process_logs.sh` using `git bisect`. 
   *Note: Since many recent commits fail to compile, your bisect automation script must handle or patch the build failure on-the-fly during the bisection process so that you can test the `process_logs.sh` logic.*
3. Once you have identified the first bad commit that introduced the incorrect log count, write its full Git SHA hash to `/home/user/bad_commit.txt`.

Ensure your final result is just the full, 40-character commit hash in `/home/user/bad_commit.txt`.