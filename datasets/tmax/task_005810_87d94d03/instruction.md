You are an MLOps engineer analyzing cross-validation artifacts. You have a log of model experiment runs in `/home/user/experiments.csv`. Each run used a specific learning rate (`lr`), and the file contains the final `accuracy` for different data folds.

You need to determine the 90% confidence interval for the mean accuracy of the *best* hyperparameter configuration using bootstrap sampling. Since bash doesn't have built-in statistical libraries, you will use standard command-line tools.

To ensure reproducibility, we have already provided the specific random indices you must use for your bootstrap samples in `/home/user/bootstrap_indices.txt`.

Perform the following steps exclusively in the terminal:
1. Parse `/home/user/experiments.csv` to find the `lr` (learning rate) that has the highest *average* accuracy across all its runs.
2. Extract the accuracy values for this best `lr`, keeping them in the exact order they appear in the CSV (this will be your population of size $N$, where the first appearance is index 1, the second is index 2, etc.).
3. Read `/home/user/bootstrap_indices.txt`. This file contains 100 lines. Each line contains a comma-separated list of 1-based indices. Each line represents one bootstrap sample.
4. For each of the 100 lines, map the indices to the accuracy values you extracted in step 2. Calculate the mean of these mapped values. Format the mean to exactly 4 decimal places (e.g., using `printf "%.4f\n"`).
5. Sort the 100 bootstrap sample means in ascending numerical order.
6. Find the 90% confidence interval by extracting the 5th value (lower bound) and the 95th value (upper bound) from your sorted list.
7. Output the final bounds to `/home/user/ci_results.txt` in exactly this format:
   `Lower: <value>, Upper: <value>`

Example of the output format:
`Lower: 0.8942, Upper: 0.9315`