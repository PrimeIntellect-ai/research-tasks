You are acting as an MLOps engineer. We have a directory of experiment artifacts (metadata) located at `/home/user/experiments`. Each artifact is a JSON file representing a trained model's hyperparameters and metrics.

Your task is to write a Go program that finds the most similar experiment to a specific target experiment based on a set of engineered features. 

The JSON files have the following structure:
```json
{
  "id": "exp_X",
  "learning_rate": 0.000,
  "batch_size": 0,
  "accuracy": 0.00
}
```

The target experiment is located at `/home/user/experiments/exp_target.json`.

Write and execute a Go script (e.g., at `/home/user/find_similar.go`) that does the following:
1. Reads all JSON files in `/home/user/experiments/`.
2. Extracts the features and creates an engineered feature vector `[f1, f2, f3]` for every experiment (including the target) using the following transformations:
   - `f1 = learning_rate * 1000.0`
   - `f2 = batch_size / 64.0` (as a floating point division)
   - `f3 = (accuracy - 0.5) * 10.0`
3. Computes the Euclidean distance between the engineered feature vector of the target experiment (`exp_target.json`) and the feature vectors of all other experiments in the directory.
4. Identifies the `id` of the experiment that is most similar (i.e., has the minimum Euclidean distance) to the target experiment. Do not compare the target experiment to itself.
5. Writes *only* the `id` string of the most similar experiment to a file located at `/home/user/most_similar_exp.txt`.

Ensure your Go code handles file reading and JSON unmarshaling properly. You can initialize a Go module in `/home/user/` if necessary.