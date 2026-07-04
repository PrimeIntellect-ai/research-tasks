You are an MLOps engineer tasked with building a lightweight data processing script to track experiment artifacts. Our latest model generates high-dimensional embeddings that need to be down-projected, validated, and logged into an experiment tracking file.

You must implement this pipeline using Go. 

The task involves the following requirements:
1. **ETL & Data Ingestion:** 
   Read a set of raw model embeddings from `/home/user/data/raw_embeddings.jsonl`. Each line is a JSON object with two fields: `id` (string) and `vector` (an array of 4 floating-point numbers).
   Read a linear projection matrix from `/home/user/data/projection_matrix.csv`. This CSV has no header and contains 4 rows and 2 columns of floats.

2. **Dimensionality Reduction:**
   Project each 4-dimensional vector down to a 2-dimensional vector by multiplying the 1x4 embedding vector by the 4x2 projection matrix.

3. **Model Output Validation:**
   We need to detect anomalous model outputs. Calculate the Euclidean norm (magnitude) of the resulting 2-dimensional vector. If the magnitude is strictly greater than `4.0`, flag the result as invalid (`false`). Otherwise, it is valid (`true`).

4. **Experiment Tracking:**
   Write the processed and validated data to `/home/user/experiment_log.tsv`. 
   The file must be a tab-separated values (TSV) file with exactly the following header line:
   `id	v1	v2	valid`
   - `id` is the document ID.
   - `v1` and `v2` are the projected coordinates, formatted to exactly 2 decimal places (e.g., `0.00`, `-5.00`).
   - `valid` is a boolean (`true` or `false`) based on the output validation step.

**Constraints & Guidelines:**
- The Go script should be self-contained and run using standard library packages only.
- Ensure the TSV columns are separated by exactly one tab (`\t`).