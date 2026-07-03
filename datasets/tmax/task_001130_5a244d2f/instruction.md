You are an automation specialist tasked with building a high-performance mathematical data pipeline. You have been given partitioned telemetry datasets, but some of the data contains critical formatting errors (specifically, embedded newlines and invalid characters in text fields) that break standard CSV parsers. 

Your goal is to write a C program and a coordinating Bash script to clean the data, merge it, compute a mathematical feature, and execute the processing in parallel.

**Data Source:**
There are 4 pairs of datasets located in `/home/user/data/`:
- `A_1.csv` through `A_4.csv` (Schema: `id,x,y,notes`)
- `B_1.csv` through `B_4.csv` (Schema: `id,z,w,status`)

**Processing Requirements:**
1. **Write a C program** (`/home/user/processor.c`) that takes two file paths as command-line arguments: `fileA` and `fileB`.
2. **Filtering (Regex):** Standard CSV parsing is failing on dataset A because some rows have corrupted `notes` fields containing embedded newlines or symbols. Your C program must read `fileA` line by line and **silently drop** any line that does not strictly match the following POSIX Extended Regular Expression:
   `^[0-9]+,-?[0-9.]+,-?[0-9.]+,[A-Za-z0-9_ ]+$`
   *(Hint: Use `<regex.h>` in C to enforce this. Any row containing an embedded newline will natively fail to match this regex on a line-by-line read).*
3. **Merging:** Read the clean rows from `fileA` and all rows from `fileB` (which is guaranteed to be clean and formatted as `^[0-9]+,-?[0-9.]+,-?[0-9.]+,[A-Za-z]+$`). Perform an inner join on the `id` column.
4. **Feature Extraction:** For each joined record, compute the Euclidean magnitude across all 4 dimensions:
   $$F = \sqrt{x^2 + y^2 + z^2 + w^2}$$
5. **Output:** The C program should print the results to `stdout` in the format `id,F`, where `F` is printed to exactly 4 decimal places.

**Workflow Automation:**
Write a Bash script at `/home/user/workflow.sh` that:
1. Compiles your C program (ensure you link the math library with `-lm`).
2. Runs the C program on all 4 pairs of files (`A_1.csv` + `B_1.csv`, `A_2.csv` + `B_2.csv`, etc.) **in parallel** as background processes.
3. Captures all standard output from these parallel runs.
4. Sorts the combined output numerically by `id`.
5. Saves the final sorted output to `/home/user/output.csv`.

Ensure your bash script is executable (`chmod +x /home/user/workflow.sh`) and runs the pipeline successfully end-to-end.