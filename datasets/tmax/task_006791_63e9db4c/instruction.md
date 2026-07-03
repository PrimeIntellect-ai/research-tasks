You are a platform engineer maintaining the CI/CD pipelines for a large multi-service architecture. We have recently refactored our pipeline configuration into modular JSON files, but our current tools cannot resolve the execution order across multiple files. 

Your task is to write a build resolution and benchmarking tool to fix this.

Step 1: Write a Python script at `/home/user/merge_and_resolve.py` that takes a directory path as a command-line argument. The script must:
- Find all `.json` files in the given directory.
- Read each file, which contains a JSON object with a `"jobs"` key. Each job maps to an object containing a `"deps"` array (a list of job names this job depends on).
- Merge all jobs into a single global dependency graph.
- Perform a topological sort to determine a valid execution order. If multiple valid orders exist, resolve ties by sorting job names alphabetically to ensure deterministic output.
- Write the final job execution order, space-separated on a single line, to `/home/user/execution_order.txt`.

Step 2: Run your script on the directory `/home/user/pipelines`. 
- There is a file called `/home/user/old_order.txt` containing the legacy, flawed execution order. 
- Create a unified diff between `/home/user/old_order.txt` and `/home/user/execution_order.txt` using the `diff -u` command. Save the output to `/home/user/order.diff`.

Step 3: Benchmark your script's performance. 
- We have generated a massive pipeline graph at `/home/user/large_pipeline`.
- Run your script against `/home/user/large_pipeline` using `/usr/bin/time -v` to capture memory and CPU profiling statistics. 
- Redirect the standard error output of the `time` command (which contains the benchmarking stats) to `/home/user/benchmark.txt`.

Requirements:
- Your Python script should only use the standard library.
- Ensure the output in `/home/user/execution_order.txt` strictly contains just the space-separated job names and a trailing newline.