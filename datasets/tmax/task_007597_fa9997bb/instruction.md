You are helping a researcher organize and preprocess a dataset of text documents using only standard Linux CLI tools (Bash, awk, sed, grep, etc.).

The raw dataset is located at `/home/user/dataset.csv`. The delimiter is the pipe character (`|`).

Your task is to write a bash script at `/home/user/pipeline.sh` that performs the following steps in a reproducible pipeline:

1. **Schema Enforcement**: Read `dataset.csv`. Keep only the rows that contain exactly 3 columns (ID, Text, Label). Discard any malformed rows (rows with fewer or more columns).
2. **Tokenization/Text Cleaning**: Convert the `Text` column (the 2nd column) of all valid rows to strictly lowercase.
3. **Dataset Splitting**: Split the valid, cleaned dataset into a training set and a testing set. The training set should contain the first 6 valid rows, and the testing set should contain the remaining valid rows.
4. **Data Leakage Prevention & Feature Engineering**: 
   - Calculate the average string length (number of characters) of the `Text` column in the **training set only**. Use integer division (truncate decimals) for the average. 
   - Note: Computing this statistic over the entire dataset before splitting is a common data leak. You must calculate it strictly on the training split.
   - Append this average length as a new 4th column to both the training and testing sets.
5. **Output**: Save the final training data to `/home/user/train_processed.csv` and the testing data to `/home/user/test_processed.csv`.

Ensure your script `/home/user/pipeline.sh` is executable and can be run to produce the outputs. Run your script to generate the final processed CSV files.

Constraints:
- Do not use Python, Perl, or any external scripting languages. Rely exclusively on shell built-ins and POSIX/GNU core utilities (awk, sed, grep, head, tail, etc.).
- The output files should maintain the `|` delimiter.