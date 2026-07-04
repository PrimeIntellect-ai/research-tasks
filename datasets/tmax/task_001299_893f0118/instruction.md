You are a storage administrator trying to free up disk space and consolidate system logs. 

You have been given a compressed archive located at `/home/user/archive.tar.gz`. This archive contains several nested `.tar` files, which in turn contain text-based `.log` files. Due to a previous storage failure, some of the nested `.tar` archives are corrupted.

Your task is to:
1. Extract `/home/user/archive.tar.gz` into `/home/user/extracted/`.
2. Identify and verify the integrity of the nested `.tar` files. You must completely ignore any corrupted `.tar` files that cannot be successfully read or extracted.
3. Extract the `.log` files from all the *valid* `.tar` archives.
4. Using Python or standard bash utilities, process the extracted `.log` files:
   - Filter out and remove any lines that contain the exact string `[DEBUG]`.
   - Concatenate the remaining lines from all valid log files into a single file at `/home/user/cleaned_logs.txt`.
   - Sort the final `/home/user/cleaned_logs.txt` file alphabetically (lexicographically) line by line.

Ensure the final file `/home/user/cleaned_logs.txt` exists and contains only the sorted, non-debug lines from the valid nested archives.