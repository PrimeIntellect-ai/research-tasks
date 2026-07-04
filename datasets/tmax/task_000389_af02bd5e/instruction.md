You are an MLOps engineer tasked with building a pipeline to track model artifacts. You have received raw system logs and need to filter, retrieve, and model the data before packaging the experiment artifact.

The raw dataset is located at `/home/user/mlops/dataset.jsonl`. 
The JSON schema for validating the data is at `/home/user/mlops/schema.json`.

Please complete the following steps:

1. **Data Schema Enforcement:** Read `/home/user/mlops/dataset.jsonl` and validate each line against `/home/user/mlops/schema.json` (you can use the `jsonschema` library). Save only the strictly valid records to `/home/user/mlops/valid_data.jsonl`, preserving their original order.

2. **Embedding Computation and Retrieval:** 
   - Extract the `message` field from the valid records.
   - Compute TF-IDF embeddings for these messages using `sklearn.feature_extraction.text.TfidfVectorizer` (use `stop_words='english'` and default parameters).
   - Embed the query string: `"critical timeout connection lost"`.
   - Calculate the cosine similarity between the query embedding and the message embeddings.
   - Retrieve the top 50 valid records with the highest cosine similarity. If there are ties, preserve the original sequence of the records.

3. **Bayesian Inference & Model Training:**
   - Using only the 50 retrieved records, extract the `features` array (which contains exactly 2 float values) as your input variables (X) and the `recovery_time` as your target variable (y).
   - Train a Bayesian Ridge regression model using `sklearn.linear_model.BayesianRidge` (with default parameters) to predict `recovery_time`.

4. **Evaluation and Artifact Packaging:**
   - Compute the Mean Squared Error (MSE) of the model's predictions on the same 50 training records.
   - Create a directory `/home/user/mlops/artifact/`.
   - Save the evaluation metric in `/home/user/mlops/artifact/metrics.json` with the exact format: `{"mse": <float_value>}`.
   - Save the model's learned coefficients (weights) in `/home/user/mlops/artifact/weights.txt` as a comma-separated string rounded to 4 decimal places (e.g., `1.2345,-0.9876`). Do not include the intercept.
   - Compress the artifact directory into a tarball at `/home/user/artifact.tar.gz` (so that extracting it yields the `artifact/` directory and its contents).

Ensure you use standard Python libraries available or installable via `pip` (like `scikit-learn`, `jsonschema`, `numpy`). You can write scripts in Python and coordinate them using Bash.