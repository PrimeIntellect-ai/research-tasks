You are a data engineer tasked with building an ETL, modeling, and benchmarking pipeline. You have been provided a dataset at `/home/user/data/raw_data.csv` which contains the following columns: `id`, `text`, `value_1`, `value_2`, `target`.

Your objective is to perform the following steps:

1. **Data Cleaning & Feature Engineering**:
   - Write a Python script to read `/home/user/data/raw_data.csv`.
   - Handle missing values in `value_1` by imputing them with the median of `value_1`.
   - Handle outliers in `value_2` by clipping the values to the 5th and 95th percentiles of `value_2` (inclusive).
   - Create a new feature `seq_length` representing the number of words in the `text` column (words are separated by whitespace).
   - Save the cleaned and processed dataset to `/home/user/data/processed_data.csv` (keep all original columns plus `seq_length`).

2. **Model Training & Benchmarking**:
   - Using the processed dataset, train a `RandomForestRegressor` from `scikit-learn` (with `random_state=42`) to predict `target` using `value_1`, `value_2`, and `seq_length` as the only input features.
   - Calculate the Mean Squared Error (MSE) of your model's predictions on the training dataset.
   - Benchmark the inference time: run the `.predict()` method on the entire processed dataset 10 separate times. Calculate the average execution time per run in seconds.
   - Save these metrics to a JSON file at `/home/user/metrics.json` with the following exact keys:
     - `"mse"`: The calculated MSE, rounded to 4 decimal places.
     - `"avg_inference_sec"`: The average inference time per run, rounded to 4 decimal places.

3. **Data Visualization (Headless)**:
   - Create a Python script at `/home/user/plot_data.py` that reads `/home/user/data/processed_data.csv` and generates a scatter plot of `seq_length` (x-axis) vs `target` (y-axis).
   - Ensure the script correctly saves the plot to `/home/user/scatter.png` without attempting to open any interactive windows, as this code will run in a headless Linux environment. Run the script to produce the image.

Ensure all required Python packages are installed (e.g., pandas, scikit-learn, matplotlib). Run your pipeline to generate all the specified output files.