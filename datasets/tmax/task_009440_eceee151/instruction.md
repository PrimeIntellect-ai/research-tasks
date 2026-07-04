I am an MLOps engineer managing a local storage repository of experiment artifacts. I suspect a data leakage issue occurred during our feature engineering pipeline, similar to a rogue `fit_transform` applied across the entire dataset. Specifically, I think at least one embedding vector in the test set is suspiciously similar (L2 distance < 0.05) to a vector in the training set. 

The embeddings are stored as plain text files, each containing a 10-dimensional mathematical vector (one floating-point number per line).
- Training artifacts are located in: `/home/user/artifacts/train/`
- Testing artifacts are located in: `/home/user/artifacts/test/`

Please write a Bash script at `/home/user/find_leak.sh` that does the following:
1. Iterates over all files in the test and train directories.
2. Computes the L2 distance (Euclidean distance) between every possible test-train file pair using standard Linux command-line utilities (like `awk`, `paste`, `bc`, etc.).
3. Finds the single pair of files where the L2 distance is strictly less than 0.05.
4. Writes the base filenames of this pair to a report file at `/home/user/leak_report.txt` in the exact format: `<test_filename> <train_filename>` (e.g., `test_12.txt train_45.txt`).

After writing the script, execute it so that `/home/user/leak_report.txt` is populated. Ensure your script is executable.