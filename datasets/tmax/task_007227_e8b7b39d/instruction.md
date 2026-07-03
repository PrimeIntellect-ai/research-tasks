You are an ML Engineer preparing and validating a simple inference pipeline. We need to test the reproducibility of a legacy C-based inference model by joining two data sources, writing a small C program to reconstruct the inference logic, and generating predictions.

Here is your task:
1. You have two feature files: `/home/user/features_a.txt` and `/home/user/features_b.txt`. Both files contain space-separated values. The first column is an integer `ID` and the second column is a float feature (`FeatureA` and `FeatureB`, respectively). The rows are NOT sorted.
2. Join these two files on the `ID` column using standard Linux command-line tools. Sort them numerically by `ID`. Save the joined result to `/home/user/joined_features.txt` in the format `ID FeatureA FeatureB` (space-separated).
3. Write a C program at `/home/user/inference.c` that reads `/home/user/joined_features.txt` line by line.
4. The C program must reconstruct our legacy linear model architecture: 
   `Prediction = (1.5 * FeatureA) - (0.5 * FeatureB) + 0.1`
5. Compile your C program to `/home/user/inference_bin` and run it. 
6. Your program should output the predictions to a log file at `/home/user/predictions.log`. Each line should be formatted exactly as `ID,Prediction`, with the prediction formatted to exactly two decimal places (e.g., `1,2.85`).

Ensure all output files (`joined_features.txt`, `inference.c`, `inference_bin`, and `predictions.log`) are in `/home/user/`.