You are a data engineer tasked with building a robust ETL pipeline using standard Linux shell tools. 

We have a dataset representing tokenized events and their associated numeric values. Some events have missing values. A previous developer tried to aggregate this data using standard bash arithmetic, which implicitly converted empty fields to `0`. This skewed our mathematical means and corrupted downstream dashboards.

Your task is to write a robust Bash pipeline that tokenizes the dataset, filters out missing data properly, and calculates accurate mathematical aggregates.

1. **Input Data**: 
A file will be located at `/home/user/raw_events.csv` with a header `ID,Tags,Value`.
- `ID`: Integer
- `Tags`: A pipe-separated (`|`) list of tokens (e.g., `error|network|timeout`)
- `Value`: An integer, or empty if the data was lost.

2. **ETL Script**:
Write a Bash script at `/home/user/etl.sh` that accepts two arguments: the input file path and the output file path.
Usage: `bash /home/user/etl.sh /home/user/raw_events.csv /home/user/summary.csv`

The script must:
- Read the input CSV.
- "Explode" the `Tags` column so that each tag gets its own record with the associated `Value`.
- **Crucially**: Completely ignore any records where the `Value` is empty (do NOT treat it as 0, which would corrupt the count and mean).
- Aggregate the data per unique tag.
- Calculate the `Sum`, `ValidCount`, and `Mean` for each tag.
- The `Mean` must be formatted as a floating-point number with exactly two decimal places (e.g., `7.50`, `12.00`), using standard rounding.
- Output the results to the specified output CSV file.

3. **Output Format**:
The output file must contain the header exactly as: `Token,Sum,ValidCount,Mean`
The rows must be sorted alphabetically by the `Token` column.
Example Output:
```csv
Token,Sum,ValidCount,Mean
alpha,15,2,7.50
beta,25,2,12.50
```

4. **Reproducibility Test**:
Write a test script at `/home/user/test_etl.sh` that generates a small dummy CSV, runs `etl.sh`, and prints "PASS" if the output is perfectly correct or "FAIL" otherwise. Ensure all scripts have executable permissions. 

You must complete this entirely using Bash, `awk`, `sed`, `bc`, or other core utilities. Do not use Python, Perl, or Ruby.