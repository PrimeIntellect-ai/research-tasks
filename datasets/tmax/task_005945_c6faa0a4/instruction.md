You are an ETL Data Engineer building a data drift monitor for a text processing pipeline. 

We need to mathematically compare a new batch of incoming text data against a baseline dataset to see if the "structural complexity" of the documents has shifted. 

You are provided with two files:
- `/home/user/baseline.txt` (the known good baseline)
- `/home/user/batch.txt` (the new incoming batch)

Write a Python script to perform the following analysis and output the results:

1. **Tokenization and Feature Extraction:**
   For each line (document) in both files:
   - Tokenize the text by splitting on whitespace.
   - Count the frequency of word lengths for lengths 1 through 10 (ignore words longer than 10 characters).
   - Represent each document as a 10-dimensional vector `[count_len_1, count_len_2, ..., count_len_10]`.

2. **Linear Algebra:**
   - Compute the L2 norm (Euclidean length) of each 10-dimensional document vector. This scalar represents the document's "complexity score".

3. **Hypothesis Testing & Confidence Intervals:**
   - Perform a two-sided Welch's t-test (unequal variances) to determine if the mean complexity score of the `batch` differs from the `baseline`.
   - Compute the 95% confidence interval for the difference in means (`Mean_batch - Mean_baseline`).
   
Output your final results into a file named `/home/user/etl_report.csv` with exactly one line containing four comma-separated values rounded to four decimal places:
`t_statistic,p_value,ci_lower_bound,ci_upper_bound`

Example output format:
`2.1054,0.0352,0.1523,4.5678`