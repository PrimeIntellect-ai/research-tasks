You are a data engineer debugging an ETL pipeline that performs a simple Bayesian anomaly detection on sensor readings. 

We have a Bash script at `/home/user/etl.sh` that is supposed to join real-time sensor readings with historical anomaly priors, calculate the posterior probability of an anomaly, and output the most anomalous sensors. 

However, much like a script that silently produces blank plots due to a backend misconfiguration, our script is currently producing a completely empty `/home/user/anomalies.txt` file despite the input data being valid. 

The input files are:
1. `/home/user/readings.csv` (Format: `sensor_id,value`) - `value` is a float.
2. `/home/user/priors.csv` (Format: `sensor_id,prior_prob`)

The pipeline should do the following using ONLY Bash, `awk`, and standard coreutils:
1. Join the two files on `sensor_id`.
2. Calculate the unnormalized posterior probability for each sensor using the formula:
   `Posterior = (1 - exp(-value)) * prior_prob`
3. Filter out any sensors where the Posterior is less than or equal to `0.5`.
4. Sort the remaining sensors by their Posterior probability in strictly descending order.
5. Save the **top 3** results to `/home/user/anomalies.txt` in the format: `sensor_id posterior_probability` (space separated).

Your task is to:
1. Identify why the current script `/home/user/etl.sh` is failing to compute the math correctly (hint: check environmental numerical library/locale configurations).
2. Fix the script so it correctly computes the values.
3. Add the missing logic to sort and extract only the top 3 results.
4. Run the script to generate the correct `/home/user/anomalies.txt`.

Ensure your final output file `/home/user/anomalies.txt` exactly matches the requested format.