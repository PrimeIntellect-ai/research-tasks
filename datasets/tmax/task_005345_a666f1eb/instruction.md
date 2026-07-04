You are a Data Scientist tasked with cleaning a dirty dataset of high-dimensional embeddings and benchmarking two different similarity search models used for down-stream inference.

You have been provided with a dataset of 2000 vectors (each 32-dimensional) located at `/home/user/dirty_embeddings.npy`. 

Your objectives are:

**Phase 1: Dataset Cleaning (Similarity Search)**
The dataset contains near-duplicates. You must clean the dataset sequentially:
1. Initialize an empty list of cleaned vectors.
2. Iterate through the `dirty_embeddings.npy` array in order (from index 0 to 1999).
3. For each vector, compute the cosine similarity against all currently stored vectors in your cleaned list. 
4. If the maximum cosine similarity between the current vector and any vector already in the cleaned list is **>= 0.92**, discard it (it's a near-duplicate). Otherwise, append it to the cleaned list.
5. Save the final cleaned array of vectors to `/home/user/cleaned_embeddings.npy` as a float32 numpy array.

**Phase 2: Inference Performance Benchmarking**
We have two simulated nearest-neighbor inference APIs in `/home/user/inference_api.py`: `infer_model_alpha(vector)` and `infer_model_beta(vector)`.
You need to benchmark their latency.
1. Randomly sample 100 vectors from your `cleaned_embeddings.npy` (use `numpy.random.seed(42)` before using `np.random.choice` on the indices, without replacement).
2. For each of the 100 vectors, run `infer_model_alpha` and record the latency (execution time) for each call. This gives you a sample of 100 latency measurements for Model Alpha.
3. Repeat the exact same process on the same 100 vectors for `infer_model_beta` to get 100 latency measurements for Model Beta.

**Phase 3: Hypothesis Testing**
Perform an independent two-sample Welch's t-test on the latency measurements to determine if there is a statistically significant difference in mean latency between Model Alpha and Model Beta.
Calculate the 95% confidence interval for the difference in means (Mean Alpha - Mean Beta).

**Reporting**
Generate a JSON report at `/home/user/report.json` with the following structure and exact keys:
```json
{
  "cleaned_count": <integer, number of vectors in cleaned_embeddings.npy>,
  "mean_latency_alpha": <float, mean of the 100 alpha latencies>,
  "mean_latency_beta": <float, mean of the 100 beta latencies>,
  "t_statistic": <float, t-statistic from Welch's t-test (Alpha vs Beta)>,
  "p_value": <float, two-tailed p-value>,
  "ci_95_lower": <float, lower bound of 95% CI for (Mean Alpha - Mean Beta)>,
  "ci_95_upper": <float, upper bound of 95% CI for (Mean Alpha - Mean Beta)>
}
```
Round all float values to 4 decimal places.

Ensure you install any necessary Python packages (like `scipy`, `numpy`, etc.) using `pip`.