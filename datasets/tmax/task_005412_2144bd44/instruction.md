You are a data engineer tasked with building a resilient data pipeline. We have a daily batch of CSV files containing telemetry data. Each CSV file has the following columns:
1. `req_id` (string)
2. `group_id` (string)
3. `timestamp` (integer)
4. `data` (string - containing a JSON-encoded object)

We process these logs using a proprietary, legacy analysis tool located at `/app/legacy_analyzer`. Unfortunately, this tool is highly unstable. It frequently crashes with a segmentation fault (exit code 139) when attempting to parse the JSON `data` column if it encounters certain malformed unicode escape sequences. The original source code for the analyzer is lost, and the binary is stripped. 

Your task is to write a Go program that acts as a strict validator and pre-processor to protect the legacy analyzer from these crashing inputs.

Requirements for your Go program (`/home/user/filter.go`):
1. **Compilation**: It must compile to an executable at `/home/user/filter`.
2. **Execution**: It must accept exactly two arguments: an input CSV file path and an output CSV file path.
   Usage: `./filter <input.csv> <output.csv>`
3. **Validation and Normalization**:
   - You must reverse-engineer or black-box test `/app/legacy_analyzer` to determine the exact nature of the unicode escape sequences in the JSON `data` that cause it to crash. (Hint: The issue is related to how the legacy C++ JSON parser handles UTF-16 surrogate pairs encoded as `\uXXXX`).
   - Read the input CSV. Tokenize and inspect the `data` column for every row.
   - If **any** row in the input CSV contains a JSON string with the crashing unicode escape condition, your program must immediately **exit with code 1** and must not create the output file. We consider this entire file "tainted" and reject it.
4. **Sorting and Grouping (The Clean Path)**:
   - If the file is completely clean (contains no crashing sequences), you must write the valid rows to the `output.csv`.
   - The output CSV must be sorted by `group_id` in **ascending** alphabetical order.
   - For rows with the same `group_id`, they must be sorted by `timestamp` in **descending** numerical order.
   - Return **exit code 0** on success.

A few sample CSV files are provided in `/home/user/samples/` for you to test against `/app/legacy_analyzer`. 

Write the complete Go program, compile it, and ensure it correctly handles large-scale files efficiently. Automated verifiers will run your compiled `/home/user/filter` against a massive corpus of both clean and malicious files.