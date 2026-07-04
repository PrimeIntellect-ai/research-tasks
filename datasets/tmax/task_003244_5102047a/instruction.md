You are an ML Engineer preparing training data for a contrastive learning model. Your task is to mine "hard negatives" for a set of anchor embeddings and statistically validate that these hard negatives are significantly more challenging than randomly sampled negatives.

You have been provided with two files containing L2-normalized embeddings (128-dimensional):
1. `/home/user/data/anchors.npy`: 500 anchor embeddings.
2. `/home/user/data/candidates.npy`: 20,000 candidate negative embeddings.

To perform the similarity search efficiently, your team uses a custom internal Python package called `fastvecsearch`. The source code for this package is vendored at `/app/fastvecsearch`.
However, the package is currently broken due to a recent bad commit. 
1. Identify and fix the bug in the `fastvecsearch` package.
2. Install the package in your environment.
3. Use the package (or your own code, but the package must be fixed and installed) to find the top 5 closest candidates (highest cosine similarity) for each anchor. These are your "hard negatives".
4. For baseline comparison, randomly sample 5 candidates per anchor to serve as "random negatives" (use `numpy.random.seed(42)` before any sampling to ensure reproducibility).
5. For each anchor, compute the mean cosine similarity of its 5 hard negatives and the mean cosine similarity of its 5 random negatives.
6. Conduct a paired t-test (using `scipy.stats.ttest_rel`) comparing the 500 hard negative means against the 500 random negative means. 
7. Calculate the 95% confidence interval for the difference between these means (Hard minus Random).

Finally, export your results to `/home/user/hard_negatives.json` with the following exact structure:
```json
{
  "hard_negative_indices": [
    [idx1, idx2, idx3, idx4, idx5], 
    ... (500 lists of 5 integers, corresponding to the anchors in order)
  ],
  "ttest_p_value": 0.0,
  "ci_lower": 0.0,
  "ci_upper": 0.0
}
```

The automated verifier will evaluate your output against the exact mathematical top-5 indices (checking for an index overlap >= 0.95) and verify your statistical test results.