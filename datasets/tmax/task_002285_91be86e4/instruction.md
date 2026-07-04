As an MLOps engineer, you need to build a lightweight Go utility to evaluate a baseline text retrieval system and track its performance metrics.

Your task is to create a Go program at `/home/user/evaluate.go` that reads a dataset, computes simple character-level "embeddings", performs cross-validation for retrieval accuracy, and benchmarks inference time. 

Here are the requirements for `/home/user/evaluate.go`:

1. **Input:** Read `/home/user/dataset.csv`. The CSV has a header and three columns: `id` (integer), `category` (string), and `text` (string). There are exactly 100 data rows (plus the header), sorted by `id`.
2. **Embedding Computation:** For each row, compute a 26-dimensional float64 vector representing the normalized frequency of English letters (a-z, case-insensitive) in the `text`. 
   - Ignore all non-alphabetic characters.
   - For example, if the text is "A b!", the vector is `[0.5, 0.5, 0, 0, ..., 0]`.
   - If a text has no alphabetic characters, the vector should be all zeros.
3. **Cross-Validation:** Perform 5-fold cross-validation. 
   - Fold 1: Test set is rows 1-20 (id 1-20), Train set is rows 21-100.
   - Fold 2: Test set is rows 21-40, Train set is rows 1-20 and 41-100.
   - ... and so on up to Fold 5.
4. **Retrieval & Inference Benchmarking:** 
   - For each test instance, find the single Nearest Neighbor in the training set using Euclidean (L2) distance on the embeddings. 
   - *Tie-breaking:* If multiple training instances have the exact same minimum distance, choose the one with the smallest `id`.
   - Measure the exact time taken to find the nearest neighbor for *each* query (only the time spent comparing distances against the training set, not embedding generation).
5. **Evaluation:** A retrieval is considered "correct" if the predicted nearest neighbor's `category` matches the test instance's `category`.
6. **Output:** The program must write a JSON file to `/home/user/metrics.json` with the following schema:
```json
{
  "folds_accuracy": [0.0, 0.0, 0.0, 0.0, 0.0], // Accuracy (between 0.0 and 1.0) for each of the 5 folds
  "mean_accuracy": 0.0, // Average of the 5 folds
  "avg_inference_us": 0 // Integer: average inference time per query across all 100 queries in microseconds
}
```

Write the code, execute it (`go run evaluate.go`), and ensure `/home/user/metrics.json` is successfully generated. Standard Go standard library packages only.