You are a data analyst tasked with building and testing a Bash-based data processing pipeline. You have been provided with two data feeds: a transactions file and an exchange rate file.

Your goal is to build a robust shell script to join these sources, calculate daily totals in USD with high numerical accuracy, and write a reproducibility test for the pipeline.

**Provided Files:**
You will find the following files in `/home/user/data/`:
1. `tx.csv` - Contains transaction records. Columns: `tx_id,date,currency,amount`
2. `fx.csv` - Contains daily exchange rates to USD. Columns: `date,currency,rate`
3. `expected.csv` - Contains the expected output for the provided sample data. Columns: `date,total_usd`

**Task Requirements:**

1. **Create the Pipeline Script (`/home/user/run_pipeline.sh`):**
   - Must be a valid, executable Bash script.
   - Must accept exactly three positional arguments:
     1. Path to transactions CSV
     2. Path to exchange rates CSV
     3. Path to output CSV
   - **Logic:** For each transaction, find the matching exchange rate for that specific `date` and `currency`. Multiply the `amount` by the `rate` to get the USD value. Sum these USD values per `date`.
   - **Output Format:** The output CSV must have the header `date,total_usd`. The rows must be sorted chronologically by date. The `total_usd` must be formatted to exactly two decimal places (e.g., `165.50`). 
   - **Constraints:** You must use standard shell tools (like `awk`, `sed`, `join`, `sort`, `bc`, etc.). Do not use Python, R, or Perl.

2. **Create the Test Script (`/home/user/test_accuracy.sh`):**
   - Must be an executable Bash script.
   - This script must execute your `run_pipeline.sh` using `/home/user/data/tx.csv`, `/home/user/data/fx.csv`, and output to `/home/user/actual_out.csv`.
   - It must then compare `/home/user/actual_out.csv` to `/home/user/data/expected.csv`. 
   - If the files match exactly (ignoring trailing newlines), the script must write the string `REPRODUCIBLE AND ACCURATE` to `/home/user/test_status.txt`.
   - If they do not match, it must write `FAIL` to `/home/user/test_status.txt`.

3. **Execution:**
   - Run your `/home/user/test_accuracy.sh` script to verify your pipeline works and to generate the final `/home/user/test_status.txt` file.

Ensure your scripts handle the headers properly and accurately calculate the floating-point math.