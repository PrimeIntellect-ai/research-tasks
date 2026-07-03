You have recently inherited a legacy mathematical codebase written in Bash, located in `/home/user/legacy_math`. The main script, `/home/user/legacy_math/calc.sh`, is supposed to read a list of numbers from `/home/user/legacy_math/inputs.txt`, square each number, multiply it by a constant found in a configuration file, and calculate the total sum using parallel background jobs to speed up the process.

However, the script is broken and produces incorrect results or errors out. You need to debug and fix it. 

Here are the known issues:
1. **Environment Misconfiguration:** The script tries to read the multiplier from a config file, but it seems to be looking in the wrong place because a specific environment variable is not set or exported correctly before the script runs. (Hint: you may need to use `strace` or read the script to see what file path it's trying to open).
2. **Format Parsing Edge-Cases:** The `inputs.txt` file was generated on a Windows system and contains carriage returns (`\r`) as well as thousands separators (e.g., `1,000` instead of `1000`). The Bash arithmetic evaluation fails on these inputs.
3. **Race Conditions:** The script uses background jobs to process the numbers concurrently, but they all read and write to a shared `/home/user/legacy_math/sum.txt` file simultaneously, causing a read-modify-write race condition that clobbers the final sum.

**Your Objective:**
1. Identify and fix the environment misconfiguration so the script successfully reads the multiplier config.
2. Modify `/home/user/legacy_math/calc.sh` to correctly parse the poorly formatted numbers in `inputs.txt` (strip commas and carriage returns).
3. Fix the concurrency bug in `calc.sh` so that the parallel background jobs do not clobber the shared sum (e.g., by using `flock`, or by having workers output to individual temporary files and summing them at the end).
4. Run the fixed script.

Save the final calculated sum to a file strictly at `/home/user/legacy_math/final_answer.txt` (just the integer value, no other text).