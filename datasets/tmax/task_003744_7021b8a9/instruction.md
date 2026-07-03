You are an MLOps engineer tasked with fixing a broken experiment tracking pipeline and exposing artifact similarity search via a REST API. 

We have a custom, vendored Python package located at `/app/mlops-artifact-utils` that handles similarity computations and visualization for our experiment metrics. However, the package is currently broken and fails to install and run in our headless container environment.

Here is what you need to do:

1. **Fix the Vendored Package**: 
   - The package is located at `/app/mlops-artifact-utils`. 
   - There are two known issues inside the package's source code:
     a) It attempts to use a GUI backend for `matplotlib` which crashes in this environment (resulting in failures or blank/un-saved plots). Change it to a headless backend (`Agg`).
     b) The core linear algebra function `cosine_similarity_matrix` in `mlops_artifact_utils/math_ops.py` contains a mathematical bug in its matrix multiplication/normalization that causes it to return incorrect results. You must identify and fix this linear algebra bug.
   - Install the fixed package into your Python environment.

2. **ETL & Visualization Pipeline**:
   - Read the experiment data from `/home/user/data/artifacts.csv`. (This file contains a header: `artifact_id,f1,f2,f3,f4,f5`).
   - Use the fixed package to generate a PCA scatter plot of the artifacts. Save the plot precisely to `/home/user/artifact_clusters.png`.

3. **Deploy the Similarity Service**:
   - Write and start a web service (using FastAPI, Flask, or Node.js) that listens on exactly `127.0.0.1:8080`.
   - The service must expose an HTTP `GET` endpoint at `/api/v1/similar`.
   - The endpoint must accept a query parameter `id` (the `artifact_id`).
   - The endpoint must require HTTP Header authentication: `Authorization: Bearer mlops-secret-77`. If missing or invalid, return a 401 Unauthorized status.
   - The endpoint should compute or lookup the top 3 most similar artifacts (excluding the queried artifact itself) using the fixed Cosine Similarity matrix. 
   - The response must be JSON in the following format:
     `{"query_id": "art_10", "top_3_similar": ["art_42", "art_8", "art_99"]}`
   - Start the service as a background process or leave it running in the terminal so our automated tests can query it.

Ensure your service is running and bound to `127.0.0.1:8080` before you finish.