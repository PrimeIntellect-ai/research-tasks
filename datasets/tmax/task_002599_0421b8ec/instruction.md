You are an AI assistant helping a data scientist fit nonlinear models to spectroscopy data. We have raw signal data that needs to be smoothed, analyzed for its peak, and evaluated with bootstrap confidence intervals. 

Additionally, the experimental metadata (containing a secret calibration token) is only available as a scanned image of a lab note. You must extract this token and use it to secure an API that you will build.

Here is your multi-step task:

1. **Extract Metadata (OCR)**
There is an image file at `/app/spectroscopy_meta.png`. Use `tesseract` (which is preinstalled) to read the text from this image. The image contains a string in the format `CALIBRATION_TOKEN=<token>`. Note this token.

2. **Process the Spectroscopy Data (Rust)**
You must create a Rust project (e.g., at `/home/user/spectro_service`) that reads `/app/raw_spectrum.csv`. The CSV has two columns, `x` (wavelength) and `y` (intensity), with a header row. 
Implement the following data processing pipeline in Rust:
- Parse the CSV data.
- Apply a moving average smoothing filter to the `y` values with a window size of 5. Specifically, for each index `i`, the smoothed value `y_smooth[i]` is the average of `y[j]` for `j` from `i-2` to `i+2`. If `j` is out of bounds (less than 0 or >= length), ignore it and average over the valid points in that window.
- Identify the peak of the signal: Find the `x` value that corresponds to the maximum `y_smooth` value. Let this be `peak_x`.

3. **Bootstrap Confidence Intervals**
To estimate the uncertainty of the peak, implement a bootstrap routine in your Rust program:
- Perform 1000 bootstrap iterations.
- In each iteration, sample $N$ rows from the original data *with replacement* (where $N$ is the number of rows in the original CSV).
- Sort the sampled data by `x` in ascending order.
- Apply the exact same moving average smoothing (window size 5) to the resampled `y` values.
- Find the `x` value corresponding to the maximum smoothed `y` in this resampled dataset.
- Collect these 1000 peak `x` values.
- Determine the 95% confidence interval by finding the 2.5th percentile and 97.5th percentile of these 1000 peak values (you can use nearest rank/index or linear interpolation, just be close). Let these be `ci_95_low` and `ci_95_high`.

4. **Expose an HTTP API**
Your Rust application must run an HTTP server listening strictly on `127.0.0.1:8080`.
- It must expose a single `GET` endpoint at `/api/analyze`.
- The endpoint must enforce an Authorization header: `Authorization: Bearer <token>`, using the exact token extracted from the image in step 1. If the header is missing or incorrect, return a 401 Unauthorized status.
- If authorized, the endpoint must execute the data processing and bootstrap routine (or return pre-computed results) and return a JSON payload with the exact following structure and keys:
  ```json
  {
    "peak_x": 45.2,
    "ci_95_low": 44.5,
    "ci_95_high": 46.1
  }
  ```

Start the server in the background and leave it running so the automated verification system can query it. You may use any Rust crates you need (e.g., `axum`, `tokio`, `serde`, `csv`, `rand`).