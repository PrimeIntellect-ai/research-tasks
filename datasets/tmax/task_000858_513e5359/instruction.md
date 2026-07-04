You are a data engineer building a robust ETL and machine learning pipeline. We recently recovered sensor logs from a damaged system, but they were only preserved as a dictated audio recording at `/app/sensor_dictation.wav`.

Your task is to build a complete automated pipeline that does the following:

1. **Audio Extraction & Parsing:**
   - Transcribe the audio file `/app/sensor_dictation.wav`. The audio contains a person reading dataset rows in a format similar to: "Row 1: Feature A 2.5, Feature B 3.1, Target 15.2".
   - Extract this transcribed data and format it into a clean CSV file named `/home/user/train_data.csv` with columns `feature_a`, `feature_b`, and `target`.

2. **Rust Machine Learning Pipeline:**
   - Create a Rust project at `/home/user/ml_pipeline`.
   - Write a Rust application that reads `train_data.csv`.
   - Use a Rust machine learning library (e.g., `smartcore` or `linfa`) to implement a Linear Regression model.
   - Implement k-fold cross-validation (k=3) within your Rust code to evaluate the model's robustness and print the mean validation Mean Squared Error (MSE) to the console as part of your experiment tracking.
   - Train the final model on the entire `train_data.csv` dataset.
   
3. **Inference / Final Step:**
   - There is a test dataset located at `/app/test_features.csv` which contains `feature_a` and `feature_b` (but no target).
   - Use your trained Rust model to predict the `target` values for these test features.
   - Output the predictions as a single column of floating-point numbers in a file located at `/home/user/predictions.txt` (one prediction per line, strictly matching the row order of `/app/test_features.csv`).

Requirements:
- Your final predictive model logic *must* be implemented in Rust.
- You may use Python, bash, or CLI tools (like `whisper` or `ffmpeg`, which you can install) for the initial audio transcription and text parsing step.
- Ensure your Rust pipeline is reproducible (use fixed random seeds if your algorithm relies on them, though standard OLS linear regression is deterministic).