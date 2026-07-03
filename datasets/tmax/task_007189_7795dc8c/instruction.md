You are helping debug a regression in a data processing pipeline.

In the directory `/home/user/data_parser`, there is a git repository containing a script called `parser.py`. This script is meant to parse a custom pipe-separated key-value data format into JSON. 

Recently, the script has started crashing when processing a slightly corrupted input file `input.txt` which contains edge cases like double pipes (`||`) and missing values (`age=`). 

We know that the commit tagged `v1.0` worked perfectly and handled these edge cases by skipping empty tokens and safely storing empty values. However, `HEAD` crashes with an error. The repository has around 200 commits between `v1.0` and `HEAD`.

Your tasks are:
1. Use git bisection to find the exact commit that introduced the regression. Write the full 40-character SHA-1 hash of this bad commit to `/home/user/bad_commit.txt`.
2. Fix the bug in `parser.py` at the current `HEAD` commit. The parser should be resilient to format errors:
   - If it encounters an empty token (e.g., caused by `||`), it should skip it.
   - If it encounters a key without a value (e.g., `age=`), it should store the value as an empty string.
   - If it encounters a token without an `=` sign entirely, it should skip it.
3. Run your fixed `parser.py` on `input.txt`. Save the resulting JSON output to `/home/user/result.log`.

Please complete these steps. Ensure that `/home/user/bad_commit.txt` contains only the commit hash and `/home/user/result.log` contains the valid JSON output.