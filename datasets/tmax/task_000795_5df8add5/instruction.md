You are a data scientist tasked with building a robust data cleaning pipeline for high-dimensional text embeddings. 

We use the `pyod` (Python Outlier Detection) library for removing anomalous embeddings. A vendored version of this package is provided at `/app/pyod-1.0.9`. However, a colleague recently introduced a deliberate perturbation in the PCA model of this vendored package to test an experimental feature, but it breaks the standard outlier detection logic.

Your tasks:
1. **Fix the Vendored Package:** Inspect `/app/pyod-1.0.9/pyod/models/pca.py`. In the `fit` method, a perturbation was introduced where the calculation of `self.decision_scores_` is artificially zeroed out or modified (e.g., multiplied by 0). Find this perturbation, restore the code to its correct mathematical implementation (using `cdist` properly as intended by PyOD), and install the package locally so your scripts can use it.
2. **Implement the Cleaning Script:** Write a Python program at `/home/user/process_embeddings.py` that reads a single JSON-encoded string from standard input (`sys.stdin.read()`).
   The input JSON will have the format:
   ```json
   {
     "embeddings": [
       [0.5, 0.1, null, 0.9],
       [0.4, 0.2, 0.3, 0.8],
       ...
     ]
   }
   ```
3. **Data Processing Steps:**
   - Convert the `"embeddings"` array to a NumPy array of type `float64`. JSON `null` values should be treated as `np.nan`.
   - **Missing Value Handling:** Impute all `np.nan` values using the *median* of their respective columns. If an entire column is `NaN`, fill it with `0.0`.
   - **Dimensionality Reduction & Outlier Detection:** Use the fixed `pyod.models.pca.PCA` class to detect outliers. Initialize the model exactly with `PCA(n_components=2, contamination=0.1, random_state=42)`.
   - Fit the model on the imputed embeddings.
   - **Filtering:** Keep only the rows that are classified as normal (where the model's `labels_` attribute equals `0`).
   - Print the resulting cleaned embeddings to standard output as a strict JSON string:
   ```json
   {
     "cleaned_embeddings": [
       [...],
       [...]
     ]
   }
   ```

Your program's standard output must exactly match the output of our reference oracle. It will be tested against hundreds of generated embedding matrices to verify bit-exact behavior. Do not print anything else to standard output.