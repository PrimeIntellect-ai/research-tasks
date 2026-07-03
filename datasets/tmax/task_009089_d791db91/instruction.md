You are tasked with building a configuration change analyzer for our infrastructure. Our configuration management system outputs an audit log of all changes in a CSV file. However, previous data pipelines failed because they silently dropped or corrupted rows containing embedded newlines and commas within fields.

Your goal is to write a robust C++ program that correctly parses this complex CSV, calculates the textual similarity between the old and new configurations, computes aggregate statistics, and stratifies the results to find the most significant changes per system category.

**Input Data:**
The input file is located at `/home/user/config_changes.csv`.
It has a header row and uses standard CSV quoting rules (fields containing commas, newlines, or double-quotes are enclosed in double-quotes. Literal double-quotes are escaped as `""`).
Columns: `Timestamp,ServerID,Category,ConfigKey,OldValue,NewValue,ChangeReason`

**Processing Requirements:**
Write a C++17 program (e.g., `analyzer.cpp`) that performs the following:
1.  **Robust Parsing:** Parse the CSV file, correctly handling embedded newlines, commas, and escaped quotes within the `OldValue`, `NewValue`, and `ChangeReason` fields. Do not use external third-party libraries (like Boost or RapidCSV); use standard C++ to build a state-machine or robust parser.
2.  **Distance Computation:** For every row, calculate the Levenshtein (edit) distance between the `OldValue` string and the `NewValue` string. 
3.  **Summary Statistics:** Calculate the average Levenshtein distance of changes for each `Category`.
4.  **Stratification / Top Changes:** For each `Category`, identify the single configuration change (row) that had the *maximum* Levenshtein distance. If there is a tie, take the one that appears first in the CSV file.

**Output Requirements:**
Your C++ program must generate two output CSV files (without headers) in `/home/user/`:

1.  `/home/user/category_stats.csv`:
    *   Format: `Category,AverageDistance`
    *   The `AverageDistance` should be rounded to exactly two decimal places (e.g., `14.50`).
    *   Sort the output alphabetically by `Category`.

2.  `/home/user/top_changes.csv`:
    *   Format: `Category,Timestamp,ServerID,ConfigKey,MaxDistance`
    *   Sort the output alphabetically by `Category`.

**Execution:**
Compile your code using `g++ -O3 -std=c++17 analyzer.cpp -o analyzer` and run it to produce the output files.