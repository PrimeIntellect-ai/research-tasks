You are an MLOps engineer responsible for verifying the integrity of experiment artifacts. A recent pipeline update generated a set of new model embedding vectors. We need to test their numerical accuracy and similarity against our baseline embeddings to track experiment drift. 

Your task is to write a Go program that performs a similarity search using linear algebra.

The environment contains two CSV files located at `/home/user/artifacts/`:
1. `baseline.csv`: Contains the canonical baseline embedding vectors. Format: `id,val1,val2,val3,val4`
2. `experiments.csv`: Contains the newly generated experiment embedding vectors. Format: `exp_id,val1,val2,val3,val4`

Write a Go script at `/home/user/evaluate.go` that does the following:
1. Parses both CSV files. The vector components (`val1` to `val4`) should be parsed as `float64`.
2. For each experiment vector, calculates the Cosine Similarity against all baseline vectors.
   *Cosine Similarity formula:* `(A · B) / (||A|| * ||B||)`
3. Identifies the closest baseline vector (the one with the highest cosine similarity) for each experiment.
4. Outputs the results to a JSON file at `/home/user/matches.json`.

The output JSON must be a serialized array of objects, sorted alphabetically by `exp_id`. Each object must exactly match this structure:
```json
[
  {
    "exp_id": "string",
    "closest_baseline_id": "string",
    "similarity": 0.9999
  }
]
```
Round the `similarity` score to exactly 4 decimal places (using standard rounding, e.g., `0.98765` -> `0.9877`).

To complete the task:
- Create the Go script at `/home/user/evaluate.go`.
- Run the script so that `/home/user/matches.json` is successfully generated.