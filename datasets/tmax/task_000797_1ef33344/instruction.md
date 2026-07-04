You are an AI data analyst investigating a series of anomalies in our server farm. We have two sources of data that need to be fused to build a predictive model. 

First, we have a large-scale storage directory containing telemetry data for thousands of servers in `/app/telemetry_data/`. This directory contains several CSV files (`server_metrics_part1.csv` to `server_metrics_part10.csv`). Each CSV has the columns: `timestamp`, `server_id`, `cpu_usage`, `memory_usage`, `disk_io`, and `network_latency`.

Second, we have an audio recording of automated alert dictations from an older legacy monitoring system, located at `/app/legacy_alerts.wav`. This audio file contains spoken English digits corresponding to `server_id`s that experienced critical temperature spikes, along with a spoken severity score (1 to 10) for each.

Your task is to:
1. Extract the `server_id`s and their corresponding severity scores from `/app/legacy_alerts.wav`. You may install and use any transcription or audio processing tools you prefer (e.g., `openai-whisper`, `ffmpeg`).
2. Aggregate the CSV telemetry data in `/app/telemetry_data/`. Compute the mean `cpu_usage`, `memory_usage`, and `disk_io` for each `server_id`.
3. Merge the aggregated CSV features with the severity scores extracted from the audio. If a `server_id` from the CSV is not mentioned in the audio, assign it a severity score of 0.
4. Train a machine learning regression model (you can use Python, scikit-learn, XGBoost, etc.) to predict `network_latency` based on the features: `cpu_usage_mean`, `memory_usage_mean`, `disk_io_mean`, and the extracted `severity_score`.
5. Save your trained model to `/home/user/latency_model.pkl` (using `joblib` or `pickle` if using Python).
6. Write a python inference script at `/home/user/predict.py` that takes a CSV file path as an argument, loads the model, and prints the predicted `network_latency` values (one per line).

You must ensure your model achieves a Mean Squared Error (MSE) of less than 0.25 on our hidden test set.