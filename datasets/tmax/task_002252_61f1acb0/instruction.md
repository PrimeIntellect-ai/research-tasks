You are an ML engineer tasked with creating a baseline model for a new dataset. To avoid any complex dependencies and to verify the logic quickly, you need to implement a 1-Nearest Neighbor (1-NN) inference pipeline using purely standard Linux command-line tools (e.g., `bash`, `awk`, `join`, `sort`).

You have been provided with three CSV files in `/home/user/`:
1. `features.csv` (columns: `id`, `feature_value`)
2. `labels.csv` (columns: `id`, `label`)
3. `split.csv` (columns: `id`, `split_name`) - where `split_name` is either `train` or `test`.

Your task is to:
1. Join the data from these three files based on the `id` column.
2. For every `id` in the `test` split, find the single closest `id` in the `train` split based on the absolute difference of their `feature_value`. 
3. If there is a tie in the absolute difference, pick the training sample with the smaller `id`.
4. Assign the `label` of the nearest training sample as the prediction for the test sample.
5. Save the predictions to `/home/user/predictions.csv`. The file must have a header `id,predicted_label` and the rows must be sorted numerically by `id`.

Constraints:
- Do not use Python, R, Perl, or any non-standard CLI tools. You must rely on shell built-ins, coreutils, and standard UNIX text processing utilities (`awk`, `sed`, `grep`, `sort`, `join`, etc.).
- The output file must perfectly match the specified format.