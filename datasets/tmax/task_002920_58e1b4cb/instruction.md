You are an MLOps engineer tasked with building a reproducible artifact tracking step for a data pipeline. The upstream pipeline occasionally produces missing values (either as `NaN` strings or completely empty fields like `,,`) which can silently corrupt downstream numerical processing and embedding retrieval.

Your task is to write a C++ program that reads experiment metrics, safely computes normalized embeddings, and logs them for experiment tracking.

**Requirements:**
1. **Input Data**: Read `/home/user/experiments.csv`. It has a header `id,v1,v2,v3` followed by data rows. 
2. **Data Imputation**: Parse the 3 numerical metrics (`v1, v2, v3`). If a value is missing (empty string) or is the string `NaN`, impute it as `0.0`.
3. **Embedding Computation**: Use the **Eigen3** C++ library (which is available at `/usr/include/eigen3`) to load the 3 metrics into an `Eigen::Vector3d`. Compute the L2-normalized embedding of this vector. *Note: If the vector's L2 norm is 0 (all elements are 0), the resulting embedding should remain `[0.0, 0.0, 0.0]` to avoid `NaN` division errors.*
4. **Tracking Output**: Save the computed embeddings to a JSON file at `/home/user/embeddings_log.json`.
   - The root must be a single JSON object.
   - Keys are the experiment `id`.
   - Values are JSON arrays containing the 3 normalized float values, rounded to exactly 4 decimal places.

**Example Output Format (`/home/user/embeddings_log.json`):**
```json
{
  "exp_1": [0.6000, 0.8000, 0.0000],
  "exp_2": [0.7071, 0.0000, 0.7071]
}
```

Write your code to `/home/user/tracker.cpp`, compile it (name the executable `/home/user/tracker`), and run it so that the JSON log is generated.