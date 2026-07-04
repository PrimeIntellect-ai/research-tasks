You are a data analyst working on a text dataset. You need to process a CSV file containing survey responses, clean the data, and compute confidence intervals.

The dataset is located at `/home/user/survey.csv` and has three columns: `id`, `group`, and `text`.

Your task is to write a C++ program (e.g., `analyze.cpp`) that reads this dataset and performs the following steps:
1. **Missing Value Handling**: Discard any rows where the `group` column is empty or contains a value other than exactly "A" or "B".
2. **Tokenization**: For the `text` column of the remaining rows, tokenize the text by splitting strictly on space characters (`' '`). Count the number of tokens (words) for each row. (e.g., "hello world" = 2 tokens).
3. **Outlier Handling**: Discard any rows where the token count is greater than 20 (these are considered outliers).
4. **Confidence Intervals**: For both Group A and Group B, calculate the sample mean, sample standard deviation, and the 95% confidence interval for the token count. Use $z = 1.96$ for the 95% confidence interval formula: $\bar{x} \pm 1.96 \times \frac{s}{\sqrt{n}}$ (where $s$ is the sample standard deviation).

Output the final results to `/home/user/summary.txt` in exactly the following format (round all numerical values to exactly two decimal places):

```
Group A: Mean=X.XX, CI=[Y.YY, Z.ZZ]
Group B: Mean=X.XX, CI=[Y.YY, Z.ZZ]
```

You may use standard Linux command-line tools to compile your C++ code. Ensure that your output strictly matches the requested format.