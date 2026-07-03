You are tasked with debugging a data processing pipeline that has recently experienced several regressions. You need to act as a developer bisecting regressions across a repository with roughly 200 commits.

The repository is located at `/home/user/data_pipeline`. 
It contains a Bash script `pipeline.sh` and some binary tools used for data processing.

Recently, two major regressions have been reported:
1. **Core Dump Regression**: The pipeline occasionally crashes with a segmentation fault (core dump). This is caused by a binary tool `filter_tool` failing on certain inputs. You need to find the exact commit where this core dump behavior was introduced.
2. **Race Condition Regression**: The Bash script `pipeline.sh` processes data files concurrently, but a race condition was introduced that causes the output file `results.txt` to have missing or interleaved lines. You need to find the commit that introduced this race condition.

Your tasks are:
1. Use `git bisect` (or manual binary search) to identify the commit hash that introduced the core dump.
2. Use `git bisect` to identify the commit hash that introduced the race condition.
3. Fix the race condition in `pipeline.sh` at the `main` branch HEAD.
4. The `filter_tool` binary lacks source code, but you must analyze the core dump or reverse-engineer the binary to figure out why it crashes. Fix `pipeline.sh` at HEAD to prepend the correct "magic header" to the data passed to `filter_tool` so that it processes the data without crashing.
5. Create a report file at `/home/user/regression_report.txt` containing exactly two lines:
   ```
   CORE_DUMP_COMMIT=<full_commit_hash>
   RACE_CONDITION_COMMIT=<full_commit_hash>
   ```

To test the pipeline, you can run `./pipeline.sh`. A successful run will produce a `results.txt` with exactly 100 lines, each formatted as `Data: <number> Processed`.

Good luck!