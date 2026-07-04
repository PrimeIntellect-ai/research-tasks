You are a data analyst tasked with building a reproducible ETL and statistical analysis pipeline in C.

You have been provided with a dataset of product reviews located at `/home/user/reviews.csv`. The file has no header and contains three comma-separated columns:
1. `review_id` (integer)
2. `rating` (integer from 1 to 5)
3. `review_text` (string, guaranteed not to contain any commas)

Your goal is to write a C program that processes this tabular data, performs tokenization on the text, and calculates a 95% confidence interval for a specific subset of the data. 

**Requirements:**
1. Create a C program at `/home/user/analyze.c`.
2. The program must read `/home/user/reviews.csv`.
3. Filter the dataset to include ONLY reviews with a `rating` of 5.
4. For these 5-star reviews, tokenize the `review_text`.
   - Use the following characters as delimiters: space (` `), tab (`\t`), newline (`\n`), period (`.`), comma (`,`), exclamation mark (`!`), question mark (`?`), semicolon (`;`), and colon (`:`).
   - Ignore empty tokens (e.g., consecutive delimiters).
5. Calculate the length of each valid token extracted from the 5-star reviews.
6. Compute the sample mean and the 95% confidence interval for the token lengths of the 5-star reviews.
   - Use the standard normal distribution approximation for the 95% CI: `Mean +/- 1.96 * (Sample Standard Deviation / sqrt(N))`
   - Use the sample standard deviation (divide by N-1 when calculating variance).
7. Create a bash script at `/home/user/run_pipeline.sh` that compiles `analyze.c` using `gcc` (with standard math library linked if needed) and runs the compiled executable.
8. The C program must output the final results to `/home/user/analysis_result.txt` in the exact following format:
```
Total 5-star reviews: <count>
Total tokens in 5-star reviews: <count>
Mean token length: <mean formatted to 4 decimal places>
95% CI: [<lower bound to 4 decimal places>, <upper bound to 4 decimal places>]
```

**Constraints:**
- Do not use any external libraries other than the C standard library (`stdio.h`, `stdlib.h`, `string.h`, `math.h`, etc.).
- Ensure your `run_pipeline.sh` is executable (`chmod +x`).

Example output format (numbers are placeholders):
```
Total 5-star reviews: 15
Total tokens in 5-star reviews: 102
Mean token length: 5.1234
95% CI: [4.8012, 5.4456]
```