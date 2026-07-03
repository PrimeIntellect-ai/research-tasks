You are a data engineer building an analytical ETL pipeline to evaluate a new semantic search model. We have exported a set of document embeddings and a set of test query embeddings to an HDF5 file. 

Your task is to build a reproducible Python pipeline that performs similarity search, extracts distance metrics, and runs a statistical hypothesis test on the results.

**Input Data:**
The file is located at `/home/user/data/embeddings.h5`. 
It contains two HDF5 datasets:
*   `corpus`: A matrix of shape (10000, 128) representing the document embeddings.
*   `queries`: A matrix of shape (50, 128) representing the query embeddings.

**Pipeline Requirements:**
1. Read the `corpus` and `queries` arrays from the HDF5 file.
2. L2-normalize both the corpus and the queries arrays (so that the L2 norm of each vector is exactly 1.0).
3. For each query, perform a similarity search to find the **top-5 nearest neighbors** in the corpus based on **Cosine Similarity** (which is equivalent to the dot product for L2-normalized vectors).
4. Extract and flatten the cosine similarity scores of these top-5 nearest neighbors across all 50 queries. You should have exactly 250 similarity scores.
5. We want to test if the mean of these top-5 similarity scores is significantly different from a baseline system's mean of `0.20`. Perform a two-sided 1-sample t-test on the 250 scores against the population mean of `0.20`.
6. Calculate the 95% confidence interval for the mean of these 250 scores.

**Output Generation:**
Your pipeline must generate a JSON file at `/home/user/pipeline_results.json` with the following schema:
```json
{
  "mean_similarity": <float>,
  "p_value": <float>,
  "ci_lower": <float>,
  "ci_upper": <float>
}
```

**Constraints:**
* Round all four float values in the JSON output to exactly **4 decimal places** (e.g., `0.1234`).
* You may install any standard Python packages (like `h5py`, `scipy`, `numpy`, `scikit-learn`) as needed.
* Ensure your mathematical operations are precise. Do not round until writing to the final JSON file.