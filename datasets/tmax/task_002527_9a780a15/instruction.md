You are a data scientist tasked with cleaning a raw dataset and evaluating the numerical accuracy and inference performance of a simple mathematical model.

The raw dataset is located at `/home/user/raw_features.csv` (contains 1000 rows and 5 columns of floating-point numbers). A set of model weights is provided at `/home/user/weights.npy`.

Your task is to write a Python script at `/home/user/pipeline.py` that performs the following:

1. **Analysis Environment Setup:** Ensure `numpy` and `pandas` are installed in your environment.
2. **ETL Pipeline:** Load the CSV file. Clip all values to be within the range `[-10.0, 10.0]`. Then apply the logistic sigmoid function $f(x) = \frac{1}{1 + e^{-x}}$ to all values.
3. **Numerical Accuracy Testing:** Perform the ETL pipeline transformations twice: once using `float64` precision for all calculations, and once using `float32` precision. Calculate the Maximum Absolute Error (Max AE) between the resulting `float64` and `float32` datasets.
4. **Inference Performance Benchmarking:** Using the `float32` cleaned dataset, perform a matrix multiplication (dot product) with the provided `weights.npy` array, and apply the sigmoid function to the result to get the final predictions. Run this inference step 1,000 times in a loop and measure the total elapsed time in seconds.

Finally, your script must output a JSON file at `/home/user/report.json` with exactly the following keys:
- `"max_abs_error"`: The Maximum Absolute Error between the float64 and float32 cleaned datasets (as a float).
- `"cleaned_data_mean"`: The mean of all values in the `float64` cleaned dataset (as a float).
- `"inference_time_sec"`: The total time taken to run the inference loop 1,000 times (as a float).

Run your script to generate the `/home/user/report.json` file.