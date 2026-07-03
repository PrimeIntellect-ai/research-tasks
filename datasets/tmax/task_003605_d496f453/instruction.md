You are a data engineer working on a high-speed ETL pipeline. We need to implement a data validation step for a database bulk export before it can be imported into our data warehouse.

You have been provided with a raw bulk export file at `/home/user/raw_export.csv`. The file is comma-separated and contains four columns: `ID`, `Name`, `Age`, and `Email`. There is no header row.

Your task is to write a fast constraint-validation program in C, and a small pipeline orchestration script in Bash to process this file.

Step 1: Write a C program at `/home/user/validator.c` and compile it to `/home/user/validator`.
The program must read CSV lines from standard input (`stdin`). For each line, it must enforce the following constraints:
1. `ID` must be a valid positive integer (ID > 0).
2. `Age` must be a valid integer between 18 and 120 (inclusive).
3. `Email` must contain at least one '@' character.

If a line passes all constraints, print it exactly as-is to standard output (`stdout`).
If a line fails one or more constraints, print it exactly as-is to standard error (`stderr`).

Step 2: Write a Bash script at `/home/user/dag_step.sh`.
This script should orchestrate this step of the pipeline. It must:
1. Execute `/home/user/validator`.
2. Feed `/home/user/raw_export.csv` into the validator's standard input.
3. Save the valid records (standard output) to `/home/user/clean_import.csv`.
4. Save the rejected records (standard error) to `/home/user/rejected.csv`.

Ensure your C program handles typical C string parsing carefully (e.g., using `strtok` or `sscanf`). Make sure both scripts are executable. Do not add any extra headers, debug text, or blank lines to the output files.