You are a data scientist tasked with cleaning and validating experimental model outputs against ground truth data. 

You have two space-separated text files, both sorted by their numeric ID:
1. `/home/user/preds.txt` containing model predictions (format: `<id> <prediction>`).
2. `/home/user/truth.txt` containing the actual target values (format: `<id> <actual>`).

Your task is to:
1. Write a Rust program at `/home/user/evaluate.rs` that reads lines from standard input (stdin). It should expect lines in the format `<id> <prediction> <actual>`. For each line, it must parse the prediction and actual values as 64-bit floats (`f64`). It should print the `<id>` to standard output (stdout) ONLY if the absolute difference between the prediction and the actual value is strictly less than `1.0`.
2. Compile this Rust program into an executable named `/home/user/evaluate`.
3. Use the bash `join` command to join `/home/user/preds.txt` and `/home/user/truth.txt` on their ID column, and pipe the joined output into your compiled `/home/user/evaluate` executable.
4. Redirect the final output (the passing IDs) into `/home/user/valid_ids.txt`.
5. Count the number of valid IDs in that file, and append a record to your experiment tracking log at `/home/user/experiment_log.txt` in the exact format: `Run 1: <count> valid models`

Ensure you use basic shell built-ins and coreutils for the data joining and file manipulation.