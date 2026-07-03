You are a data engineer working on an ETL pipeline that cleans incoming sensor data, processes it through a simple pre-trained Multi-Layer Perceptron (MLP), and generates automated plots and performance benchmarks. 

Your colleague started writing the script `/home/user/etl_pipeline.py` to process `/home/user/sensor_data.csv` using the model weights in `/home/user/model_weights.json`. However, the script is incomplete and buggy:
1. **Missing values and outliers:** The data contains `NaN` values and extreme outliers. The script currently fails when processing them.
2. **Model architecture:** The NumPy-based MLP inference function is missing its non-linear activation function.
3. **Plotting issues:** The script attempts to generate a matplotlib scatter plot, but it crashes or produces blank plots because the server is a headless Linux environment.
4. **Benchmarking:** The pipeline needs to measure the inference time.

Your task is to fix and complete `/home/user/etl_pipeline.py` so that it successfully runs and does the following:

**1. Data Cleaning:**
- Load `/home/user/sensor_data.csv`.
- Impute any missing (`NaN`) values in the 'X' column using the **median** of the non-missing values in that column.
- After imputation, clip the 'X' values to be strictly within the range `[-10.0, 10.0]` to handle outliers.

**2. Model Inference:**
- The network is a 1-hidden-layer MLP (Input -> Hidden(Size 2) -> Output). 
- Fix the `predict(X_clean, weights)` function. The hidden layer must use a **ReLU** (Rectified Linear Unit) activation function before multiplying by the second layer's weights.
- Run the cleaned 'X' data through the model to generate predictions.

**3. Performance Benchmarking:**
- Measure the time it takes to run the `predict` function on the entire dataset. (Record the elapsed time in seconds).

**4. Outputs:**
- **Plot:** Save a scatter plot of Cleaned 'X' (x-axis) vs Predictions (y-axis) to `/home/user/inference_plot.png`. Ensure matplotlib is configured correctly for a headless environment so the plot actually renders and saves.
- **Metrics Report:** Save a JSON file to `/home/user/pipeline_metrics.json` with exactly the following keys:
  - `"median_imputed"`: The median value used for imputation (float).
  - `"mean_prediction"`: The mean of the final predicted values (float).
  - `"inference_time_seconds"`: The time taken for the inference step (float).

Run your script to produce `/home/user/inference_plot.png` and `/home/user/pipeline_metrics.json`.