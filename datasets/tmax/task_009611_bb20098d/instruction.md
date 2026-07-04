You are an MLOps engineer tasked with cleaning and analyzing a collection of experiment artifact metadata.

In the directory `/home/user/artifacts/`, there are several JSON files, each representing an experiment run. Some of these runs contain corrupted telemetry or missing fields.

Your objective is to:
1. **Schema Enforcement & Outlier Handling:** Read all JSON files in `/home/user/artifacts/`. A valid run must contain:
   - `run_id` (string)
   - `description` (string)
   - `metrics` (dictionary) containing EXACTLY two keys: `accuracy` (float) and `loss` (float).
   Filter out any runs that are missing these fields. Further, filter out any runs where `accuracy` is an outlier (defined as less than 0.0 or greater than 1.0) or where `loss` is missing or negative.
2. **Embedding & Similarity Search:** For the *valid* runs only, extract the `description` text. Use `scikit-learn`'s `TfidfVectorizer` (with default parameters) to compute the text embeddings for these valid descriptions. 
3. **Recommendation:** Given the target query: `"Optimized deep neural network for image classification"`, transform this query using the fitted vectorizer and compute the cosine similarity between the query and all valid runs.
4. **Reporting:** Find the top 3 valid runs with the highest cosine similarity to the query. Write their `run_id`s to `/home/user/top_runs.txt`, one per line, in descending order of similarity.

Ensure your Python script cleanly handles the data processing and similarity computation, and outputs strictly the 3 IDs to the text file.