You are an automation specialist creating a data processing workflow. We have a pipeline that processes mathematical expressions, but the input dataset often contains different expressions that evaluate to the exact same result (e.g., "10 * 5" and "100 - 50"). 

Your task is to create a Python ETL script at `/home/user/process_math.py` that reads these expressions, deduplicates them based on their mathematical result, logs the pipeline execution, and generates a final report using a text template.

Here are the exact requirements for `/home/user/process_math.py`:

1. **Read Input**: Read the file `/home/user/data/expressions.txt`. Each line contains one mathematical expression.
2. **Evaluate and Hash**: Evaluate each expression mathematically. To handle deduplication robustly, format the numerical result as a string rounded to exactly 4 decimal places (e.g., `"50.0000"`), and compute its MD5 hash.
3. **Deduplicate**: Filter out duplicate expressions based on this MD5 hash. Only keep the *first* expression encountered for each unique hash.
4. **Pipeline Logging**: Write a log entry to `/home/user/pipeline.log` exactly in this format:
   `INFO: Processed <TOTAL_LINES> lines, found <DUPLICATE_COUNT> duplicates.`
5. **Template Generation**: Read the template file `/home/user/template.md`. 
   - Replace the placeholder `{{UNIQUE_COUNT}}` with the integer number of unique expressions kept.
   - Replace the placeholder `{{EXPRESSIONS_LIST}}` with a newline-separated list of the kept expressions and their evaluated results (formatted to 1 decimal place). Format each line as: `<original_expression> = <result_1_decimal>` (e.g., `10 * 5 = 50.0`). Maintain the original order of first appearance.
6. **Output**: Save the finalized text to `/home/user/report.md`.

Run your script to produce `/home/user/report.md` and `/home/user/pipeline.log`.