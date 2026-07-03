You are an AI assistant helping a data scientist set up a Rust-based data cleaning and validation microservice.

We have a vendored Rust crate located at `/app/outlier_detect`. This crate provides a single utility function: `outlier_detect::filter_outliers(data: &[f64]) -> Vec<f64>`, which removes values that are more than 2 standard deviations away from the mean. However, the package is currently broken due to a deliberate perturbation in its source code (a syntax or configuration error). Your first job is to fix the vendored package so it compiles successfully.

Next, you need to create a Rust web service in `/home/user/data_service` that uses this vendored package. 
Initialize a new Rust project there and implement an HTTP server that listens on `127.0.0.1:8080`.

The service must implement the following:
- **Endpoint**: `POST /process`
- **Authentication**: Must require an HTTP header: `Authorization: Bearer secret_token_999`. Return `401 Unauthorized` if missing or incorrect.
- **Input Payload**: A JSON array of objects representing a dataset. Schema: `[{"id": integer, "val": float or null}, ...]`
- **Processing Steps**:
  1. **Schema Enforcement & Missing Values**: Parse the JSON. Calculate the mean of all *present* (non-null) `val` fields. Impute any `null` `val`s with this calculated mean.
  2. **Outlier Handling**: Extract all the `val`s (now fully populated) into a slice/vector, and pass them to `outlier_detect::filter_outliers` to remove outliers.
  3. **Bootstrap Confidence Interval**: Take the cleaned `val`s. Perform a bootstrap analysis by taking 1,000 resamples (with replacement) of the same size as the cleaned array. Calculate the mean of each resample. Find the 5th and 95th percentiles of these 1,000 bootstrapped means.
- **Output Payload**: Return a JSON response with the HTTP 200 status code:
  `{"cleaned_count": <integer_number_of_items_after_outlier_removal>, "mean_ci": [<5th_percentile_float>, <95th_percentile_float>]}`

You may use popular Rust crates like `axum`, `tokio`, `serde`, `serde_json`, and `rand` to build the service. Make sure your server runs continuously in the background or foreground so we can test it using HTTP requests once you indicate you are finished. 

To complete the task:
1. Fix the vendored package at `/app/outlier_detect`.
2. Write and run the Rust web service at `127.0.0.1:8080`.