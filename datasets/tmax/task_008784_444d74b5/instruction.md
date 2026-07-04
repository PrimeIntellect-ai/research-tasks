You are a data engineer building a lightweight ETL pipeline to process a stream of text data. You need to write a Python script `/home/user/process.py` that reads a tab-separated file located at `/home/user/input.tsv`.

The input file contains two columns without a header:
1. `category` (a string)
2. `raw_text` (a string containing mixed characters and punctuation)

Your Python script must perform the following pipeline steps in order:

1. **Tokenization and Normalization**: 
   For each line, extract the `raw_text`. Normalize it by converting it to lowercase and removing all characters EXCEPT alphanumeric characters (`a-z`, `0-9`) and spaces. Then, tokenize the normalized text by splitting on single spaces. Filter out any empty tokens. Calculate the `token_count` for this text.

2. **Data Sampling and Stratification**: 
   Process the lines in the exact order they appear in the file. Stratify the data by `category` and sample (keep) ONLY the first 3 entries for each category. Discard any subsequent entries for a category once it has reached 3 samples.

3. **Rolling Statistics Computation**: 
   For the sampled entries, calculate a 2-period rolling average of the `token_count` independently for each `category`. 
   - For the first entry in a category, the rolling average is simply its own `token_count`.
   - For the second and third entries, the rolling average is the arithmetic mean of the current entry's `token_count` and the previous sampled entry's `token_count` for that category.

**Output:**
Write the results to a CSV file at `/home/user/output.csv` with the following headers:
`category,normalized_text,token_count,rolling_avg`

The `normalized_text` should be the tokens joined by a single space.
The `rolling_avg` must be formatted to exactly one decimal place (e.g., `2.0`, `2.5`).
The rows in the output CSV must be in the same relative order as they were sampled from the input file.

Ensure your script runs successfully and produces the output file.