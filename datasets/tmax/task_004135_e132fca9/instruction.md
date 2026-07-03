You are a Data Engineer building an analytical ETL serving layer. Your goal is to process data from multiple sources, perform statistical and dimensionality reduction tasks on the fly, and serve the results via an HTTP API.

You have been provided with two data sources in the `/app/` directory:
1. `/app/sensor_metadata.png`: An image containing a scanned table with the columns `sensor_id` and `location`.
2. `/app/sensor_readings.csv`: A CSV file containing sensor telemetry with columns `sensor_id`, `temp`, `pressure`, `vibration`, and `output_metric`.

**Your instructions:**
1. Extract the text from the image (you may use `tesseract` which is pre-installed) to recover the `sensor_id` to `location` mapping.
2. Join this metadata with the telemetry data in `sensor_readings.csv` on `sensor_id`.
3. Create and start an HTTP web server listening on `127.0.0.1:8000`.
4. Your server must expose an endpoint: `GET /api/v1/sensor_stats?location=<location_name>`
5. When the endpoint is called, it should filter the joined dataset for the given location and calculate the following:
    * **PCA Explained Variance:** Fit a Principal Component Analysis (PCA) model to reduce the `temp`, `pressure`, and `vibration` columns to 1 component. (Do not scale the data before fitting). Extract the explained variance ratio of this first component.
    * **Bootstrap Confidence Interval:** Calculate the 95% confidence interval for the mean of the `output_metric` column using the bootstrap method (1000 resamples, random seed = 42).
    * **Hypothesis Testing:** Perform a 1-sample t-test (two-sided) to check if the mean of the `output_metric` for this location differs from a population baseline of `50.0`. Extract the p-value.
6. The endpoint must return a JSON response exactly like this (round all numerical values to 3 decimal places):
```json
{
  "location": "North_Wing",
  "pca_explained_variance": 0.981,
  "bootstrap_ci_95": [48.123, 51.456],
  "ttest_p_value": 0.045
}
```

Ensure your server remains running in the background or foreground so that it can be tested. You can use any language or framework (e.g., Python with Flask/FastAPI/pandas/scikit-learn/scipy).