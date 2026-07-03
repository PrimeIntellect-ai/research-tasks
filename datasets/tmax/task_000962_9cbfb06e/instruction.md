You are an open-source maintainer reviewing a PR for a data processing CLI. A contributor has submitted a Bash script (`/home/user/migrate_v1_to_v2.sh`) to perform a schema migration on user data. The goal is to migrate data from the V1 format to the V2 format, which involves evaluating a raw mathematical expression for each user.

However, the contributor's PR is broken and has three major flaws:
1. **Memory Inefficiency:** It attempts to load the entire dataset into memory at once using command substitution (`$(cat ...)`), which causes Out-Of-Memory (OOM) errors on large datasets.
2. **Expression Evaluation Failure:** It incorrectly uses `expr` to evaluate the formulas, failing on floating-point numbers and complex order of operations.
3. **Missing Schema Headers:** It completely strips out the schema headers during processing and fails to emit the required V2 header.

Your task is to fix the script and process a sample file.

**Requirements:**
1. Refactor `/home/user/migrate_v1_to_v2.sh` so that it streams the input file line-by-line (or uses stream processing tools like `awk` within the bash script) instead of buffering the whole file. 
2. Fix the expression parsing and evaluation. Ensure mathematical formulas in the 3rd column are evaluated accurately, respecting floating-point arithmetic. Format the evaluated result to exactly 2 decimal places (e.g., `3.33`).
3. The script must take the input file path as its first argument (`$1`).
4. The script must output the migrated data to stdout. The first line must be the new V2 header: `id|name|calculated_value`. Subsequent lines should contain the evaluated data.
5. Run your fixed script against the sample dataset located at `/home/user/v1_data.txt` and redirect the standard output to `/home/user/v2_data.txt`.
6. To prove to the PR author that your streaming approach fixes the memory leak, profile your script's execution. Run the script against `/home/user/v1_data.txt` using `/usr/bin/time -v` and redirect the profiling output (stderr) to `/home/user/memory_profile.txt`.

The original `/home/user/v1_data.txt` contains:
```
id|name|raw_math_formula
1|Alice|3.5 * 2.0
2|Bob|10 / 3
3|Charlie|2.5 + 4.1 * 2
4|David|100 - 15.75
```