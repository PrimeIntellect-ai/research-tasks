You are a data engineer building an ETL pipeline. Your goal is to write a Python script that validates incoming text records against a set of "golden" reference records using text embeddings and bootstrap sampling to establish dynamic thresholds.

You have two input files (you will need to assume they exist, but they will be placed in your environment):
1. `/home/user/golden_records.txt` - A list of verified, high-quality product descriptions (one per line).
2. `/home/user/incoming_records.txt` - A list of new, unverified product descriptions (one per line) coming from the ETL stream.

Write a script at `/home/user/validate_etl.py` that performs the following steps:

1. **Embedding Computation:** Read the golden records. Use `sklearn.feature_extraction.text.TfidfVectorizer` (with default parameters) to fit and transform the golden records into TF-IDF vectors (our "embeddings").
2. **Numerical Configuration & Sampling:** To establish a valid similarity threshold, we will bootstrap a distribution of expected similarities between valid items. 
   - Set the random seed exactly via `import numpy as np; np.random.seed(42)`
   - Generate 1000 random pairs of indices from the golden records using `np.random.choice(len(golden_records), size=(1000, 2), replace=True)`.
   - Calculate the cosine similarity (using `sklearn.metrics.pairwise.cosine_similarity`) between the two TF-IDF vectors for each of the 1000 pairs.
   - Calculate the 5th percentile of these 1000 similarity scores using `np.percentile(scores, 5)`. This value is your `validation_threshold`.
3. **Model Output Validation (Retrieval):** Read the `incoming_records.txt`.
   - Transform the incoming records using the *already fitted* `TfidfVectorizer`.
   - For each incoming record, compute its cosine similarity against *all* golden records and find the maximum similarity score.
   - If a record's maximum similarity score to the golden dataset is strictly less than the `validation_threshold`, flag its status as `INVALID`. Otherwise, flag it as `VALID`.
4. **Reporting:** Write the results to `/home/user/validation_results.csv` with the following format:
   - A header row: `record_id,status,max_similarity`
   - `record_id` is the 0-indexed line number of the incoming record.
   - `status` is either `VALID` or `INVALID`.
   - `max_similarity` is the maximum similarity score formatted to exactly 4 decimal places (e.g., `0.1234`).

Run your script to produce the output file. Note: Empty lines in the input files should be ignored, and only non-empty lines should be counted for indexing.