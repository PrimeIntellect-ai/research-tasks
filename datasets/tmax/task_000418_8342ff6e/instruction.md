You are a data analyst migrating a legacy risk scoring pipeline. We have a compiled proprietary binary, `/app/risk_oracle`, which processes CSV data from standard input (stdin) and outputs the scored data to standard output (stdout). We need to replace this binary with an equivalent Python script.

The binary reads a CSV containing two columns: `text_data` and `base_prior`. 
- `text_data` contains tokenized text (tokens separated by the `|` character).
- `base_prior` is a float between 0.01 and 0.99 representing the prior probability of a risk event.

The binary outputs a CSV with an additional third column, `posterior`, formatted to 4 decimal places.

Through some preliminary reverse engineering, we've determined the following about the binary's internal algorithm:
1. It reads the CSV from stdin (including the header).
2. For each row, it tokenizes `text_data` by splitting it using `|`.
3. It computes a "feature embedding" for each token, which is simply its character length.
4. It treats each token as an independent event to update the `base_prior` using Naive Bayes.
5. The likelihood of a token given the positive class is defined as: `L_pos = max(0.01, min(length / 100.0, 0.99))`.
6. The likelihood of a token given the negative class is `L_neg = 1.0 - L_pos`.
7. It applies the standard Bayesian update rule sequentially for each token to find the final posterior probability.
8. It prints the original columns plus the `posterior` column.

Your task:
Write a Python script at `/home/user/solution.py` that replicates this exact behavior. It must read from stdin and write to stdout. The output must be bit-for-bit identical to what `/app/risk_oracle` produces given the same input. 

You can test `/app/risk_oracle` to observe its exact output format. Make sure your Python script is executable or can be run via `python3 /home/user/solution.py`.