You are acting as a Data Analyst processing sensor reliability data. We need to build a data processing pipeline in Go that performs Bayesian inference to update failure probabilities based on current readings, and identifies similar sensors using similarity search.

You have been provided with a dataset at `/home/user/sensors.csv`. The CSV has a header and the following columns:
1. `sensor_id` (string)
2. `val_x` (float64) - Spatial X coordinate
3. `val_y` (float64) - Spatial Y coordinate
4. `prior_fail` (float64) - Prior probability that the sensor is in a failed state: $P(Fail)$
5. `p_high_given_fail` (float64) - Likelihood of a high-temperature reading if the sensor has failed: $P(High | Fail)$
6. `p_high_given_ok` (float64) - Likelihood of a high-temperature reading if the sensor is OK: $P(High | OK)$
7. `is_high` (int) - The current reading status (1 = High Temp, 0 = Normal Temp)

Your task:
1. Create a Go module and write a program at `/home/user/process.go` that parses this CSV file.
2. For each sensor, calculate the **posterior probability of failure** given its current `is_high` reading, using Bayes' Theorem.
   - If `is_high == 1`, calculate $P(Fail | High)$.
   - If `is_high == 0`, calculate $P(Fail | Normal)$ (Note: $P(Normal | State) = 1 - P(High | State)$).
3. For each sensor, find the `sensor_id` of its **nearest neighbor** (the single most similar *other* sensor) based on the Euclidean distance of their spatial coordinates (`val_x` and `val_y`).
4. Write the results to `/home/user/results.csv` with the exact header: `sensor_id,posterior_fail_prob,nearest_sensor_id`.
   - The `posterior_fail_prob` must be rounded to exactly 4 decimal places (e.g., `0.3077`).
5. Compile your code to `/home/user/process` and execute it so the results file is generated.

Ensure your code handles calculations with strict numerical accuracy. Do not use any external third-party Go packages for math or CSV parsing; rely entirely on the standard library.