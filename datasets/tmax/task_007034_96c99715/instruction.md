You are an MLOps engineer responsible for managing and validating a large-scale repository of machine learning experiment artifacts. Recently, we suspect that some of our experiments suffer from a "data leakage" bug, similar to calling `fit_transform` on a test set instead of just `transform`.

You have a directory at `/home/user/artifacts/` containing several JSON files. Each JSON file represents a logged artifact from a specific phase of an experiment. 

Your task is to write a Go program, saved at `/home/user/detect_leakage.go`, that processes these JSON files, enforces a strict schema, and identifies which experiments suffer from data leakage. 

### Requirements:

1. **Schema Enforcement:** 
   Your Go program must parse the JSON files and strictly enforce the following schema. Any file not conforming to this exact structure (e.g., missing fields, incorrect types) should be ignored.
   - `experiment_id` (string): Unique identifier for the experiment.
   - `phase` (string): Must be either `"train"` or `"test"`.
   - `feature_mean` (float64): The mean of the data split.
   - `scaler_val` (float64): The scaling value applied to the data split.

2. **Data Leakage Detection:**
   An experiment consists of exactly one `"train"` artifact and exactly one `"test"` artifact (paired by `experiment_id`). 
   Data leakage occurred if the test set was improperly fit on itself. Specifically, an experiment has leaked if the `scaler_val` in the `"test"` phase is exactly equal to the `feature_mean` of the `"test"` phase. (In a correct experiment, the `"test"` phase's `scaler_val` should strictly equal the `"train"` phase's `feature_mean`).

3. **Output:**
   Your program must write a file at `/home/user/leaked_experiments.txt` containing the `experiment_id` of every experiment that has data leakage.
   - Write one `experiment_id` per line.
   - The IDs must be sorted alphabetically.
   - You must only use Go standard libraries (e.g., `encoding/json`, `os`, `path/filepath`, `sort`).

Run your Go program to generate the output file.