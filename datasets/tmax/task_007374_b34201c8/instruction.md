You are a researcher organizing a dataset of vector embeddings. You've noticed that data leakage often occurs when standardizing (Z-score normalizing) features before splitting them into train and test sets.

Your task is to demonstrate the quantitative difference between a "leaky" normalization and a "strict" normalization pipeline using purely standard Linux command-line tools (Bash, `awk`, `bc`, etc.). Python, R, and other high-level scripting languages are strictly forbidden for this task.

You are provided with a dataset at `/home/user/embeddings.csv`. It has a header and four columns: `id,split,v1,v2`. The `split` column contains either `train` or `test`.

Write a bash script at `/home/user/analyze.sh` that calculates a specific covariance-like metric for the `test` set under two scenarios:

**Scenario 1: Leaky**
1. Calculate the population mean and population standard deviation for `v1` and `v2` using the **entire** dataset (both train and test).
2. Normalize the `test` split values using these global statistics: $v'_{leaky} = \frac{v - \mu_{all}}{\sigma_{all}}$
3. Calculate the average product of the normalized test features: $Metric_{leaky} = \frac{1}{M} \sum_{i \in test} (v1'_{i, leaky} \times v2'_{i, leaky})$ where $M$ is the number of test samples.

**Scenario 2: Strict**
1. Calculate the population mean and population standard deviation for `v1` and `v2` using **only the train** split.
2. Normalize the `test` split values using these train-only statistics: $v'_{strict} = \frac{v - \mu_{train}}{\sigma_{train}}$
3. Calculate the average product of the normalized test features: $Metric_{strict} = \frac{1}{M} \sum_{i \in test} (v1'_{i, strict} \times v2'_{i, strict})$

**Output Format**
Your script `/home/user/analyze.sh` must be executable and, when run without arguments, output exactly two lines rounding the final metrics to 4 decimal places:
```
LEAKY: <value>
STRICT: <value>
```

Constraints:
- Do not use Python, Perl, Ruby, or Node.js.
- Standard tools like `awk`, `sed`, `grep`, `bc`, `paste` are allowed and encouraged.
- Ensure you compute the *population* standard deviation (divide by N, not N-1).