You are an MLOps engineer responsible for maintaining the integrity of machine learning experiment artifacts. Your team runs massive cross-validation pipelines with Bayesian hyperparameter tuning, and the resulting metrics are dumped as JSON files. However, some runs fail silently, producing missing values, invalid schemas, or extreme outliers.

Your task is to write a Go program `/home/user/validate.go` that reads all JSON experiment artifacts in `/home/user/artifacts/`, enforces a data schema, filters out invalid or outlier runs, and outputs the valid experiment IDs.

The JSON artifacts have the following expected schema:
```json
{
  "experiment_id": "string",
  "hyperparameters": {
    "learning_rate": "float",
    "prior_alpha": "float",
    "prior_beta": "float"
  },
  "metrics": {
    "cv_score": "float (can be missing/null in bad runs)"
  }
}
```

A valid experiment must meet ALL the following conditions:
1. Valid Schema & Missing Value Handling: All fields mentioned above must exist. The `cv_score` must not be null, missing, or 0.
2. Bayesian Priors Check: `prior_alpha` and `prior_beta` must both be strictly greater than `0.0`.
3. Outlier Handling: `cv_score` must be between `0.50` and `0.99` (inclusive). Any score outside this range is considered a divergent outlier.
4. `learning_rate` must be strictly between `0.0` and `1.0`.

Write the Go script to iterate over all `.json` files in `/home/user/artifacts/`. For every file that passes all the above checks, extract the `experiment_id`.
Finally, write the valid `experiment_id`s to `/home/user/valid_experiments.txt`, with one ID per line, sorted alphabetically.

Execute your script to generate the output file.