You are an ML engineer working on a data preparation pipeline. Your colleague left an unfinished and buggy Python script at `/home/user/ml_pipeline/prepare_data.py`. 

The pipeline is supposed to:
1. Load `raw_data.csv` from `/home/user/ml_pipeline/`.
2. Generate a heatmap of the correlation matrix and save it. Currently, the script runs but generates a completely blank plot. Fix the plotting logic so `correlation_plot.png` actually contains the plot (hint: look at the order of matplotlib commands or backend usage).
3. Filter highly correlated features. You need to implement the `filter_features` function. It should compute the Pearson correlation matrix. For any pair of features with an absolute correlation > 0.85, drop the feature that appears later in the DataFrame's column order.
4. Balance the dataset using bootstrap sampling. Implement the `bootstrap_balance` function to upsample the minority class in the `target` column so its count equals the majority class. Use sampling with replacement and set `random_state=42` for reproducibility.
5. Train a Random Forest classifier and evaluate it. Implement `train_evaluate`. Train a `RandomForestClassifier(random_state=42)` on the balanced data. Compute the F1 score on the provided test set and write the float value to `/home/user/ml_pipeline/metrics.txt` (just the number, e.g., `0.952`).
6. Save the final balanced and filtered training DataFrame to `/home/user/ml_pipeline/processed_data.csv`.

Fix and complete `/home/user/ml_pipeline/prepare_data.py`, then run it to produce the outputs. Ensure all requested output files (`correlation_plot.png`, `processed_data.csv`, `metrics.txt`) are generated correctly.