You are a Data Analyst tasked with fixing and completing a microservice-based data processing pipeline. 

There are two existing services provided in `/app`:
1. A Redis server intended to serve user multiplier configurations.
2. A Flask API serving a regression model (located in `/app/api/app.py`).

Your task has two parts:

**Part 1: Service Composition & Fixes**
The startup script `/app/start_services.sh` is supposed to launch Redis and the Flask API. However, the configurations are slightly mismatched.
- Redis must run on `127.0.0.1:6379`. (Check `/app/redis.conf` and adjust as necessary).
- The Flask API must run on `127.0.0.1:5000`. You may need to modify its startup parameters or fix missing dependencies to ensure it runs correctly when `bash /app/start_services.sh` is executed.
Ensure both services are running in the background before proceeding.

**Part 2: The Pipeline Script**
Create a Python script at `/home/user/pipeline.py`. This script will process a single row of CSV/JSON data provided as a command-line argument.

**Invocation:**
`python3 /home/user/pipeline.py '{"user_id": 105, "v1": 12.5, "v2": 4.2}'`

**Script Logic:**
1. **Parse Input:** Parse the single JSON string argument containing `user_id` (int), `v1` (float), and `v2` (float).
2. **Feature Engineering & Bootstrap:** 
   Create a base feature array of 4 elements: `[v1, v2, v1 - v2, v1 + v2]`.
   Perform a deterministic bootstrap to calculate an `engineered_feature`.
   - Initialize Python's built-in random number generator with the user ID: `rng = random.Random(user_id)`.
   - Generate exactly 100 resamples (each of size 4) from the base feature array. (Use `rng.choices(base_array, k=4)`).
   - Calculate the mean of each resample.
   - The `engineered_feature` is the mean of those 100 means.
3. **Cache Lookup:**
   Query the local Redis server (db=0) for the key `multiplier_<user_id>`. 
   If it exists, parse it as a float. If it does not exist, default to `1.0`.
   Calculate `final_feature = engineered_feature * multiplier`.
4. **Model Inference:**
   Send a POST request to `http://127.0.0.1:5000/predict` with the JSON payload: `{"feature": final_feature}`.
   The API will return a JSON response: `{"prediction": <float>}`.
5. **Output:**
   Print the exact prediction value returned by the API, formatted to exactly 4 decimal places (e.g., `42.1230`). Do not print anything else to standard output.

Make sure your script perfectly adheres to this mathematical and procedural flow, as it will be rigorously tested against thousands of randomized inputs.