You are a researcher organizing a text dataset. You need to implement a basic hyperparameter tuning script to evaluate the optimal dimensionality for a character-frequency embedding model, using nearest-neighbor retrieval.

Your task is to write a Go program at `/home/user/organizer.go` and run it to produce an experiment tracking log.

### Dataset
The dataset is located in `/home/user/dataset/` and is split into two directories:
- `/home/user/dataset/train/` (Training files)
- `/home/user/dataset/val/` (Validation files)

### Embedding Logic
You will compute a simple "embedding" vector for each `.txt` file. 
An embedding of dimension `D` (where `1 <= D <= 26`) is a `float64` slice of length `D`.
The value at index `i` (0-indexed) is the count of the `i`-th letter of the lowercase English alphabet in the file's content. All text should be converted to lowercase before counting. Characters outside 'a'-'z' are ignored.
For example, if the text is "apple banana" and `D=3`, the counts for 'a', 'b', 'c' are 4, 1, 0, so the embedding is `[4.0, 1.0, 0.0]`.

### Nearest-Neighbor Retrieval & Error Metric
For a given dimension `D`:
1. Compute the embeddings (length `D`) for all files in the `train` set and all files in the `val` set.
2. For each validation embedding, find the *nearest neighbor* in the training set embeddings using standard Euclidean distance.
3. The "error" for dimension `D` is the sum of the Euclidean distances from each validation embedding to its nearest training embedding.

### Experiment Tracking
Your Go program must evaluate all possible dimensions `D` from 1 to 26 inclusive.
It should write an experiment log to `/home/user/experiment_log.json`. This file must contain a JSON array of objects representing the hyperparameter tuning results, like so:
```json
[
  {"D": 1, "error": 1.23},
  {"D": 2, "error": 4.56},
  ...
]
```
*Note: Round the `error` to exactly 2 decimal places in the JSON output.*

Finally, the program must write the integer value of the best `D` (the one that produced the lowest error) to a text file at `/home/user/best_model.txt`. If there is a tie for the lowest error, choose the smaller `D`.

### Environment
- Run your Go program and ensure `/home/user/experiment_log.json` and `/home/user/best_model.txt` are generated successfully.