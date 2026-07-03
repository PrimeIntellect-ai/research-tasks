You are a Data Engineer building a reproducible ETL and machine learning pipeline for monitoring server health. 

You have been given a raw dataset at `/home/user/data/server_metrics.jsonl`. Each line in this file is a JSON object with nested structures. 

Your tasks are:
1. **Dependency Management**: Install any necessary libraries (e.g., pandas, scikit-learn) you need to complete the task. You may use any programming language.
2. **Data Processing (ETL)**: Write a script that parses the JSONL file. Extract the following features from the nested `metrics` object: `cpu_utilization`, `memory_gb`, and `disk_io`. The target variable should be extracted from the `status` object: set the target to `1` if `error_code` is greater than `0`, and `0` otherwise.
3. **Modeling**: Implement a Logistic Regression classifier to predict the target using the extracted features. The pipeline must scale the features using standardization (zero mean, unit variance) before fitting the model. 
4. **Reproducibility & Experiment Tracking**: Your script must accept two arguments: a random seed and a regularization parameter `C`.
   - Use the random seed for both the train/test split (test_size=0.25) and the Logistic Regression initialization.
   - Train the model and calculate the accuracy on the test set.
   - Append the results to an experiment tracking file at `/home/user/pipeline_runs.jsonl`. Each run should append a single JSON object with the exact keys: `{"seed": <int>, "C": <float>, "accuracy": <float>}`. Round accuracy to 4 decimal places.

Run your pipeline to conduct the following three experiments:
- Experiment 1: seed = 42, C = 1.0
- Experiment 2: seed = 42, C = 0.1
- Experiment 3: seed = 99, C = 1.0

Ensure that by the end of your process, `/home/user/pipeline_runs.jsonl` exists and contains exactly three lines corresponding to these experiments.