You are an ML Engineer preparing data for a model. An upstream data processing pipeline has a bug where it occasionally introduces NaNs or silently converts integer columns to floating-point formats (e.g., `102.0` instead of `102`) when merging datasets.

We need a fast, compiled tool to strictly validate the schema of the target column before training begins. 

Write a C++ program at `/home/user/validate_int.cpp` that reads a standard comma-separated file (CSV) and enforces a strict integer schema on a specific column.

Requirements for the C++ program:
1. It should take two command line arguments: the file path, and the 0-based column index to check. 
   Example: `./validate_int /home/user/data.csv 2`
2. It must skip the first line (the header).
3. For all subsequent lines, it must check the specified column index.
4. A value is considered a **valid integer** if and only if:
   - It is not empty.
   - It contains only digits (0-9).
   - It may optionally start with a single minus sign (`-`).
   - It does NOT contain decimal points (`.`), `NaN`, spaces, or any other characters.
5. If a row's target column value violates this schema, print the 1-based line number of that row to standard output.

Once you have written the C++ program:
1. Compile it to an executable named `/home/user/validate_int` (use `g++ -O3`).
2. Run it against the dataset located at `/home/user/dataset.csv`, checking column index `2`.
3. Redirect the output (the list of invalid 1-based line numbers) to `/home/user/invalid_rows.txt`.

Ensure `/home/user/invalid_rows.txt` contains exactly one line number per line, sorted in ascending order.