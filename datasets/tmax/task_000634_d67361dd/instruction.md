You are an AI assistant acting as a Data Engineer. You need to build a critical mathematical transformation step in our Python ETL pipeline. 

Your task is to create a Python script at `/home/user/run_etl.py` that processes a stream of text logs, calculates the Bayesian posterior probability of an anomaly ("urgent" state), and tracks the pipeline execution metrics using MLflow.

Here are the specific requirements:
1. **Dependencies**: You may need to install `mlflow` and any standard mathematical libraries you need.
2. **Inputs**:
   - A dataset of log messages exists at `/home/user/raw_logs.csv` (Columns: `id`, `message`).
   - A configuration file for our Bayesian filter exists at `/home/user/config.json`. It contains the prior probability of an urgent message (`prior_urgent`) and the likelihoods of specific token keywords occurring in both "urgent" and "normal" messages.
3. **Data Processing & Tokenization**:
   - Read the CSV file.
   - Tokenize each message by lowercasing the text, removing all punctuation (replace with spaces), and splitting by whitespace to get a set of unique words per message.
4. **Bayesian Inference**:
   - Implement a Naive Bayes calculator. For each message, calculate the posterior probability that the message is "urgent".
   - Use the prior from the config. (Note: $P(Normal) = 1 - P(Urgent)$).
   - For the likelihoods, only consider words in the message that exist in the config's `likelihoods` dictionary. If a word from the config is present in the message, multiply the running likelihood by $P(word | class)$. Ignore words not in the config.
   - Calculate the exact normalized posterior probability: $P(Urgent | words)$.
5. **Output**:
   - Filter the messages to keep only those where the posterior probability of being "urgent" is strictly greater than `0.5`.
   - Save these messages to `/home/user/urgent_logs.json`. The output should be a JSON array of objects, e.g., `[{"id": 1, "posterior": 0.9143}, ...]`. Round the posterior to exactly 4 decimal places.
6. **Experiment Tracking**:
   - Use `mlflow` to track this ETL run.
   - Set the MLflow tracking URI to a local directory: `file:///home/user/mlruns`
   - Create or use an experiment named `ETL_Anomaly_Detection`.
   - Start an MLflow run.
   - Log the parameter `prior_urgent` (from the config).
   - Log the metric `urgent_count` (the number of messages that passed the > 0.5 threshold).

Write and execute this script so the system achieves the described final state. Ensure all files and directories are created in the exact locations specified.