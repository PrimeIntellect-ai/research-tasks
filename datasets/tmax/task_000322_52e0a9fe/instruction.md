I need your help organizing a dataset of experimental sensor readings, fixing a broken inference library, and setting up an API to serve a Bayesian model.

Here are the specific steps you need to complete:

1. **ETL & Correlation Analysis**:
   - I have a raw dataset at `/home/user/sensor_data.csv` containing columns: `sensor_A`, `sensor_B`, `sensor_C`, `sensor_D`, and `target`.
   - Write a Python script to compute the Pearson correlation matrix of the four sensors.
   - Find the sensor (B, C, or D) that has the highest absolute correlation with `sensor_A`. Drop that highly correlated sensor from the dataset to reduce redundancy.
   - Calculate the determinant of the covariance matrix of the remaining *three* sensors.
   - Save your experiment tracking results to `/home/user/tracking.json`. The JSON must have exactly this structure:
     ```json
     {
       "dropped_sensor": "sensor_X",
       "covariance_determinant": 0.12345
     }
     ```

2. **Fix the Vendored Package**:
   - We use a proprietary package called `bayes_prob_lib` located at `/app/bayes_prob_lib`.
   - Unfortunately, it's currently broken. The `Makefile` in the package has an indentation error (it uses spaces instead of tabs), preventing it from building the C-extensions if you try to run `make`. Also, the main file `bayes_prob_lib/inference.py` attempts to use `np.exp()` but mistakenly imports numpy as `import numpy as n`. 
   - Fix these issues and install the package in the local environment (e.g., using `pip install -e /app/bayes_prob_lib` after fixing the Makefile and running `make`).

3. **Reconstruct Model & Serve API**:
   - Create a web server using Flask or FastAPI that listens on exactly `127.0.0.1:8000`.
   - The server must expose a `POST /infer` endpoint.
   - The endpoint must require an `Authorization` header with the exact value `Bearer lab_auth_token_88`. If missing or incorrect, return a 401 Unauthorized status.
   - The endpoint will receive JSON payloads with the three retained sensors, for example: `{"sensor_A": 1.2, "sensor_C": 0.5, "sensor_D": -1.1}`.
   - Inside the endpoint, use the fixed library to calculate the posterior. The library exposes a function: `bayes_prob_lib.inference.calculate_posterior(sensor_dict)`. (Assume the library handles the internal Bayesian network architecture based on the 3 keys passed).
   - Return a JSON response in this format: `{"posterior_probability": 0.852}` (where 0.852 is the float returned by the library).

Leave the server running in the background when you are done so that the automated test can verify it.