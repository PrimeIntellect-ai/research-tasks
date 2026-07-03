You are an MLOps engineer tracking acoustic experiment artifacts. We have an acoustic sensor dataset from a recent machine run, stored as a WAV file at `/app/sensor_data.wav`. We also have the target performance metric for each 1-second interval of the audio recorded in `/app/targets.csv`.

Your objectives are:

1. **Fix the Visualization Script:** 
   There is a script at `/app/visualize.py` intended to plot the raw waveform of the first second of the audio and save it to `/home/user/waveform.png`. However, it currently produces empty or broken images due to a matplotlib backend misconfiguration. Debug and fix this script, then run it so that `/home/user/waveform.png` is correctly generated and shows the waveform.

2. **Build an ETL & Modeling Pipeline:**
   Create a reproducible Python script at `/home/user/pipeline.py` that performs the following steps:
   - Load the audio file `/app/sensor_data.wav`.
   - Segment the audio into non-overlapping 1-second chunks.
   - Extract at least two basic time-domain features for each chunk. We recommend RMS (Root Mean Square) energy and Zero-Crossing Rate (ZCR).
   - Load the target variable from `/app/targets.csv` (each row corresponds to a 1-second chunk in chronological order).
   - Compute the Pearson correlation between your extracted features and the target variable to ensure they are predictive (you may print this to the console).
   - Perform an 80/20 Train-Test split on the dataset (using `random_state=42`, no shuffling since it's time-series-like, so `shuffle=False`).
   - Train a `LinearRegression` model from `scikit-learn` using your extracted features to predict the target variable.
   - Evaluate the model on the test set using Mean Squared Error (MSE).
   - Save the test MSE into a JSON file at `/home/user/metrics.json` with the exact key `"test_mse"`.

Ensure your environment has the necessary libraries (e.g., `scipy`, `numpy`, `pandas`, `scikit-learn`, `matplotlib`). You may install them if they are missing.