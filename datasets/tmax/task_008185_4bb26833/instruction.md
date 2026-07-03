You are a data engineer building an ETL pipeline. We need to analyze the relationship between the lengths of text in two separate columns of a dataset. 

You have a raw dataset located at `/home/user/etl_raw.tsv`. This file contains two columns of text separated by a tab (`\t`).

Your task is to:
1. Write a C program at `/home/user/compute_cov.c` that reads pairs of integers from standard input (one pair per line, separated by whitespace) until EOF. It must calculate the **sample covariance** of these two variables and print the result to standard output, formatted to exactly 3 decimal places (e.g., `-1.234`).
2. Compile your C program to `/home/user/compute_cov`.
3. Using standard bash shell utilities (like `awk`, `sed`, `tr`, etc.), write a command or short script to:
   - Read `/home/user/etl_raw.tsv`.
   - Tokenize the text in each column by spaces (i.e., count the number of space-separated words/tokens in the first column, and the number of space-separated words/tokens in the second column for each line). Empty columns or extra spaces should be handled appropriately (assume standard word splitting).
   - Pipe these pairs of integer counts into your compiled `/home/user/compute_cov` program.
4. Save the final output of the C program to `/home/user/covariance_result.txt`.

Ensure your C code accurately computes the sample covariance (divide by N-1).