You are a Machine Learning Engineer preparing a robust training pipeline. Your team uses a proprietary, compiled feature extractor binary located at `/app/bin/feature_extractor` to convert raw text logs into numerical feature vectors for downstream model training. 

Recently, the team discovered a critical data leakage bug: certain malicious or malformed text logs trigger an undocumented edge case in the binary, causing it to leak global test-set statistics into the output feature vector. These corrupted vectors poison the training data.

We have isolated two sets of raw log files:
- `/app/data/clean/`: Contains logs that process normally.
- `/app/data/evil/`: Contains logs that trigger the data leakage bug in the extractor.

Your objective:
1. Analyze the behavior of `/app/bin/feature_extractor` on both the clean and evil corpora. The binary takes a single file path as an argument and prints a JSON list of numerical features to standard output (e.g., `./feature_extractor log.txt`).
2. Identify the anomaly in the extracted features that indicates leakage, and trace it back to the patterns in the raw text logs.
3. Write a Python script at `/home/user/detector.py` that acts as a standalone data filter. 

Requirements for `/home/user/detector.py`:
- It must take a single raw log file path as a command-line argument.
- It must analyze the raw text directly and determine if it is clean or evil.
- It **MUST NOT** call or depend on `/app/bin/feature_extractor`. The evaluation environment will not have the binary installed.
- If the log is clean, print exactly `CLEAN` to standard output and exit with status code 0.
- If the log is evil (would trigger the leak), print exactly `EVIL` to standard output and exit with status code 1.
- You may use scikit-learn or standard Python libraries to build heuristics or a small model, but the script must run entirely offline and standalone.

Ensure your detector is perfectly accurate on the provided corpora before concluding the task.