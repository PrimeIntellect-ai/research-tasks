You are a data analyst working entirely in the Linux terminal. Your team uses a proprietary, pre-compiled black-box machine learning model located at `/app/model_predictor`. 

This binary takes raw data from standard input (comma-separated, without a header) and outputs exactly one floating-point prediction per line. However, the binary is highly sensitive: it expects exactly 4 integer features per line and will crash or return garbage if it encounters missing values (empty strings).

You have been given a training dataset:
- Features: `/home/user/data/train_features.csv`
- Labels: `/home/user/data/train_labels.csv`

Your objectives:
1. Conduct an experiment entirely using Bash and standard Linux text utilities (e.g., `awk`, `sed`, `bc`). You must determine the best missing-value imputation strategy for the 4 features. Evaluate strategies like imputing missing values with 0, or with the column's mean (rounded to the nearest integer). 
2. Write a final Bash script at `/home/user/predict.sh`.
   - The script must take exactly one argument: the path to an input CSV file (e.g., `/home/user/predict.sh /home/user/data/val_features.csv`).
   - The script must preprocess the CSV by imputing any missing values (represented by `,,` or trailing `,`) using the optimal strategy you discovered. Keep in mind that the binary expects strictly integers, so silently introducing floats (e.g., 2.5) will degrade the binary's internal math.
   - The script must pipe the cleaned data to `/app/model_predictor`.
   - The script must output the predictions to standard output (one prediction per line).

Ensure your preprocessing is robust and relies only on Bash/standard utilities. An automated verifier will evaluate your script against a held-out test set and calculate the Mean Squared Error (MSE) of your predictions. Your script's output must achieve an MSE below a specific threshold to pass.