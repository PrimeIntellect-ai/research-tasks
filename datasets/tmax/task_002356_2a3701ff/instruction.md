You are an expert data scientist. We have a batch of raw IoT sensor data that needs to be cleaned, validated, and analyzed for anomalies using a Bayesian probabilistic model. Finally, the inference step needs to be benchmarked to ensure it can run efficiently in production.

Your goal is to build a reproducible Python pipeline to process this data. 

**Data Source:**
There is a raw dataset located at `/home/user/raw_sensor_data.csv` containing the following columns: `timestamp`, `sensor_id`, `temperature`, `humidity`.

**Phase 1: Data Schema Enforcement**
Write a Python script (`/home/user/step1_clean.py`) that reads `/home/user/raw_sensor_data.csv` and strictly enforces the following schema:
1. `timestamp`: string (can be ignored for validation, just pass it through).
2. `sensor_id`: integer.
3. `temperature`: float, must be between -50.0 and 50.0 (inclusive).
4. `humidity`: float, must be between 0.0 and 100.0 (inclusive).

Any row that contains missing values, cannot be cast to the correct type, or falls outside the allowed numerical bounds must be dropped entirely. 
Save the resulting valid records to `/home/user/clean_data.csv` (keeping the original headers).

**Phase 2: Bayesian Anomaly Detection**
Write a script (`/home/user/step2_inference.py`) that reads `/home/user/clean_data.csv` and performs Bayesian anomaly detection on the `temperature` readings grouped by `sensor_id`.

Assume the following probabilistic model for temperature:
- Prior distribution for the mean temperature of any sensor: $\mu \sim \mathcal{N}(\mu_0 = 20.0, \sigma_0^2 = 25.0)$
- Observation model (likelihood) for temperature readings $x_i$ from a sensor given its mean $\mu$: $x_i \sim \mathcal{N}(\mu, \sigma^2 = 4.0)$

For each `sensor_id`:
1. Calculate the posterior distribution of the mean, $\mu_n \sim \mathcal{N}(\mu_{post}, \sigma_{post}^2)$, using all valid temperature readings for that specific sensor. 
   - Recall the Bayesian conjugate update for a Normal prior and Normal likelihood:
     - $1/\sigma_{post}^2 = 1/\sigma_0^2 + n/\sigma^2$
     - $\mu_{post} = \sigma_{post}^2 \cdot (\mu_0/\sigma_0^2 + \sum_{i=1}^n x_i / \sigma^2)$
     - where $n$ is the number of readings for that sensor.
2. Form the posterior predictive distribution for observations: $x \sim \mathcal{N}(\mu_{post}, \sigma_{post}^2 + \sigma^2)$.
3. Flag any reading $x_i$ for that sensor as an anomaly if its absolute difference from $\mu_{post}$ is strictly greater than $3 \times \sqrt{\sigma_{post}^2 + \sigma^2}$.

Output all anomalous rows (with their original columns) to `/home/user/anomalies.csv`. Keep the CSV headers.

**Phase 3: Inference Benchmarking**
Write a script (`/home/user/step3_benchmark.py`) that loads `/home/user/clean_data.csv` into memory, and then measures the execution time of the Bayesian anomaly detection logic (Step 2 calculations) over the *entire clean dataset*. 
- Run the inference process 100 consecutive times in a loop.
- Calculate the average time taken per run in milliseconds.
- Save this single numerical value (rounded to 2 decimal places) to `/home/user/benchmark.txt`.

**Phase 4: Reproducible Pipeline**
Create a Bash script at `/home/user/run_pipeline.sh` that sequentially executes Phase 1, Phase 2, and Phase 3. The script must be executable.

Ensure you install any Python libraries you might need (like `pandas` or `scipy`). You are allowed to use standard data science libraries.