You are an MLOps engineer tasked with recovering an old experiment and exposing its tracking metrics via a local web service. 

We have lost the original configuration file, but we have a screenshot of the terminal when the experiment was run, located at `/app/experiment_config.png`.

Your task is to:
1. Extract the `EXPERIMENT_SEED` (an integer) and `TARGET_VARIANCE` (a float) from the image `/app/experiment_config.png`. You can use OCR tools like `tesseract` for this.
2. Write a reproducible Python pipeline that does the following:
   - Generates a synthetic dataset using `sklearn.datasets.make_classification(n_samples=1000, n_features=50, n_informative=30, random_state=EXPERIMENT_SEED)`.
   - Fits a Principal Component Analysis (PCA) model on this dataset to reduce its dimensionality. The number of components should be the minimum required to retain a ratio of variance equal to or strictly greater than the `TARGET_VARIANCE` extracted from the image.
   - Transforms the dataset using this PCA model.
   - Computes the covariance matrix of the PCA-transformed dataset (using `numpy.cov` with `rowvar=False`).
3. Create and start a local HTTP API (using Flask, FastAPI, or similar) that exposes these experiment metrics.
   - The service must listen on `127.0.0.1:5000`.
   - The service must require a custom HTTP header for all requests: `X-MLOps-Auth: track-me`. Requests without this header or with an incorrect value should return a 401 or 403 status code.
   - Endpoint `/config` (GET): Return a JSON object with the extracted parameters and the number of PCA components kept: `{"seed": <int>, "target_variance": <float>, "n_components": <int>}`.
   - Endpoint `/covariance` (GET): Return a JSON object with the top-left 2x2 elements of the computed covariance matrix. Use the keys: `{"cov_00": <float>, "cov_01": <float>, "cov_10": <float>, "cov_11": <float>}`. Round floats to 4 decimal places.
4. Start the web service in the background. Once the service is fully running and ready to accept requests, create an empty file at `/home/user/server_ready.txt`.

Ensure your code is strictly reproducible by using the exact random seed extracted from the image.