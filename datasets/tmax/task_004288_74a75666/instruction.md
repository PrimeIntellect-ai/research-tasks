You are an MLOps engineer troubleshooting an experiment tracking pipeline. Recent updates have introduced a silent data corruption issue where some integer ID columns were converted to floats or `NaN` values due to a faulty Pandas transformation.

You have a set of experiment logs located in `/home/user/experiments/`. Each file is a CSV containing hyperparameter cross-validation results and the resulting linear model weights.

The CSVs have the following header:
`run_id,param_alpha,cv_fold_1,cv_fold_2,cv_fold_3,w_1,w_2,w_3`

Your task is to analyze these artifacts entirely using Bash shell built-ins and standard POSIX CLI tools (like `awk`, `grep`, `sed`, `bc`, etc. Python or other scripting languages are not allowed). 

Follow these steps:
1. **Schema Enforcement**: Identify and exclude any CSV files that contain schema violations. A file is invalid if *any* value in its `run_id` column (excluding the header) is not a strict integer (e.g., `105.0` or `NaN` are invalid; only formats like `105` are valid). If a file has even one invalid `run_id`, exclude the entire file from the next steps.
2. **Cross-Validation Evaluation**: For all rows in the *valid* CSV files, calculate the mean cross-validation score across the three folds: `(cv_fold_1 + cv_fold_2 + cv_fold_3) / 3`.
3. **Hyperparameter Selection**: Find the single `run_id` with the highest mean cross-validation score among all valid files.
4. **Linear Algebra**: For this best `run_id`, calculate the L2 norm of its weight vector `[w_1, w_2, w_3]`. The L2 norm is the square root of the sum of the squared vector values: `sqrt(w_1^2 + w_2^2 + w_3^2)`.
5. **Reporting**: Write the best `run_id`, its mean CV score, and its weight L2 norm to `/home/user/best_model_stats.txt` in a comma-separated format: `run_id,mean_cv,l2_norm`. Format the `mean_cv` and `l2_norm` strictly to 4 decimal places (e.g., `103,0.9100,1.0000`).

Ensure your final output file strictly matches the requested format.