You are an MLOps engineer tasked with analyzing experiment artifact logs to detect data leakage in our machine learning pipelines. We have a problem where some pipelines apply transformations (like `fit_transform` or tokenization) to the entire dataset before splitting it into train and test sets, causing data leakage.

First, examine the image located at `/app/leak_rule.png`. It contains the exact textual rule defining what constitutes a "leakage" in our system's pipeline logs.

Next, you need to write a detector script at `/home/user/detect_leak.py` (or a bash script `/home/user/detect_leak.sh`) that reads a pipeline log file and determines whether it contains a data leakage according to the rule extracted from the image.

The log files are simple text files where each line represents a pipeline operation (e.g., `load_data`, `train_test_split`, `fit_transform_scaler`, `predict`). 

Your script must:
1. Accept exactly one command-line argument: the path to a log file.
2. Parse the log file.
3. Exit with status code `1` (reject) if the log violates the rule (i.e., it contains data leakage).
4. Exit with status code `0` (accept) if the log is clean.

To help you develop and test your script, we have provided two directories of sample logs:
- `/app/samples/evil/`: Contains logs that have data leakage.
- `/app/samples/clean/`: Contains clean logs.

Your final solution must correctly classify 100% of the unseen logs that the verification system will test it against. Ensure your script is executable (`chmod +x`).