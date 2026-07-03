You are acting as a capacity planner analyzing resource usage for a legacy cluster. You need to automate the extraction of data from an old interactive monitoring console, clean the data using shell utilities, and write a Rust application to project future capacity requirements. 

Complete the following steps in order:

**1. Idempotent Environment Setup**
Create an idempotent bash script at `/home/user/init_env.sh`. When run, it must:
- Ensure the directory `/home/user/capacity_planner/data` exists.
- Ensure a new Cargo (Rust) binary project is initialized at `/home/user/capacity_planner/predictor` (do not overwrite `Cargo.toml` or `src/main.rs` if they already exist).
- Exit with code 0.

**2. Expect Scripting for Interactive Automation**
There is a legacy python script located at `/home/user/legacy_monitor.py`. When executed via `python3`, it behaves interactively:
- It prompts: `Enter cluster name: ` -> You must send `ALPHA_CLUSTER`
- It prompts: `Enter days of history: ` -> You must send `7`
- It then prints a block of messy text containing the logs and exits.

Write an Expect script at `/home/user/capacity_planner/fetch.exp` that automates this interaction. It must capture the output and save *only* the standard output of the python script into `/home/user/capacity_planner/data/raw.txt`. 

**3. Text Processing Pipeline**
The `raw.txt` file will contain header junk, footer junk, and data lines formatted loosely with spaces and pipes. 
Example of a data line: `[INFO] | node-01 | CPU: 45.2 | MEM: 1024`
Write a bash script at `/home/user/capacity_planner/clean.sh` that reads `/home/user/capacity_planner/data/raw.txt` and uses text processing utilities (like `awk`, `sed`, or `grep`) to generate a clean CSV at `/home/user/capacity_planner/data/clean.csv`. 
The CSV must have exactly this format (no header row):
`node_name,cpu_value,mem_value`
For the example above, it should output: `node-01,45.2,1024`
Ignore all lines that do not start with `[INFO] |`.

**4. Rust Capacity Predictor**
Write a Rust program in `/home/user/capacity_planner/predictor/src/main.rs`.
The program must:
1. Read `/home/user/capacity_planner/data/clean.csv`.
2. For each unique `node_name`, calculate the **average** CPU usage and **average** Memory usage across all entries for that node.
3. Calculate a "Projected" value by adding 20% to the average (i.e., multiply the average by 1.2).
4. Output a JSON file at `/home/user/capacity_planner/report.json` with the following exact structure:
```json
{
  "node-01": {
    "avg_cpu": 45.2,
    "avg_mem": 1024.0,
    "projected_cpu": 54.24,
    "projected_mem": 1228.8
  }
}
```
*Note: Format floating-point numbers in the JSON output to 2 decimal places if needed, but standard f64 JSON serialization is acceptable as long as the math is correct.*

Execute your scripts and the Rust program to generate the final `report.json`.