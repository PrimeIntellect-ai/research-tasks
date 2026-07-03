You are a performance engineer tasked with fixing a broken Go-based log analysis tool. 
The tool is located in `/home/user/perf-tool`. It reads system performance logs from `/home/user/data/perf.log` and calculates an aggregated metric score.

Currently, the tool cannot even compile, and if you force it to run, it crashes or produces incorrect results. 

Your goals are to debug and fix the tool so that it accurately computes the average performance score. Specifically, you need to:

1. **Resolve the dependency issue:** The project fails to build because of a bad dependency version in `go.mod`. You must identify the invalid version and update it to a valid, working version (e.g., the standard stable version `v0.9.1` for the errors package).
2. **Fix boundary conditions:** The tool crashes on certain malformed log lines in `perf.log`. Update the code to safely ignore any line that does not have exactly 4 comma-separated fields.
3. **Correct the mathematical formulas:** 
   - The score calculation formula is implemented incorrectly. The comments in the code state: "Score = 50% CPU, 10% Memory". However, the code uses a different multiplier for memory. Fix the multiplier.
   - The final average calculation contains an off-by-one error. It currently divides by `count - 1`. It should divide by the exact `count` of valid lines processed.

Once you have fixed the code, compile and run the tool. 
Take the final outputted "Average Score" (which is printed to stdout) and save exactly that number (just the number, e.g., `123.45`) to `/home/user/solution.txt`.

Do not modify the `perf.log` file. All fixes must be made in the Go source code or `go.mod`.