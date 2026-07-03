You are tasked with debugging and fixing a regression in a custom Bash-based text encoding tool. 

A Git repository is located at `/home/user/encoder_repo`. It contains the source code for a pure-Bash text encoder script named `encode.sh`. Over the last 200 commits, multiple developers have added features, optimizations, and extensive logging to this script. However, a regression was introduced somewhere in the commit history: the script no longer correctly encodes certain strings, failing silently or producing corrupted output compared to our gold-standard compiled binary.

We have provided the original, working compiled C reference implementation (stripped of debugging symbols) at `/app/oracle_processor`. 

Your objectives are:
1. **Analyze the Oracle:** Analyze `/app/oracle_processor` (using tools like `strings`, `objdump`, or by running it) to understand the exact input format it expects (it requires a specific magic header before it processes text) and its output behavior.
2. **Bisect the Regression:** Use `git bisect` in `/home/user/encoder_repo` to find the exact commit that introduced the encoding corruption. You will likely need to write an automated bisection script that feeds test strings (derived from your analysis of the binary) to both `encode.sh` and `/app/oracle_processor` and compares the diffs.
3. **Fix the Bug:** Once you identify the bad commit and understand the logic flaw (e.g., incorrect string manipulation, broken regex, or mishandled memory/variables in the Bash script), check out the `main` branch (`HEAD`), and fix `encode.sh`.
4. **Deploy:** Save your fully fixed script to `/home/user/fixed_encode.sh`. Ensure it has execute permissions. 

Your fixed script at `/home/user/fixed_encode.sh` must be a drop-in replacement that exactly matches the output of `/app/oracle_processor` for all valid inputs. An automated test suite will evaluate your script's correctness against the oracle on a held-out dataset of edge cases.