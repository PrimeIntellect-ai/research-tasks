You are tasked with writing a bash script that performs a mathematical data-processing pipeline. We need to find the sum of the intersection of two large sets of numbers stored in JSON format, but we must use a specific local version of `jq` to ensure compatibility, and we need to benchmark the calculation phase.

Write a bash script at `/home/user/process_sets.sh` that does the following:

1. **Local Dependency Management**: The system's package manager is off-limits. Your script must create the directory `/home/user/bin/` if it doesn't exist, and download the `jq` 1.6 binary for linux64 directly from `https://github.com/jqlang/jq/releases/download/jq-1.6/jq-linux64`. Save it exactly as `/home/user/bin/jq` and make it executable. 
2. **Deserialization**: Use this specific `/home/user/bin/jq` binary to read two files: `/home/user/data/set_A.json` and `/home/user/data/set_B.json`. Both files contain a JSON object with a single key `"numbers"` pointing to an array of integers (e.g., `{"numbers": [10, 5, 100]}`).
3. **Sorting & Diffing**: Extract the arrays, sort them numerically, and find the intersection (the exact mathematical set of numbers that appear in both files).
4. **Mathematical Operation**: Calculate the total sum of these intersecting numbers.
5. **Benchmarking**: The specific commands that perform the intersection and summing must be timed using `/usr/bin/time -p`. 

**Output Requirements:**
- The final calculated sum must be saved to `/home/user/sum.txt`.
- The `time -p` standard error output (which contains the `real`, `user`, and `sys` times) must be saved to `/home/user/benchmark.txt`.
- The script must be executable. When run, it should perform all the above steps automatically.

Ensure your script handles standard paths and uses standard bash tools (like `comm`, `sort`, `awk`, or `bc`) alongside the downloaded `jq` binary.