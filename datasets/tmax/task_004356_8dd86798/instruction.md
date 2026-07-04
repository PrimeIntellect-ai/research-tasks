I am a researcher organizing a massive dataset of IoT telemetry logs. Unfortunately, some of our sensors were compromised, injecting anomalous readings into the dataset. I need to separate the clean logs from the compromised ones using an old Bayesian scoring model we have lying around.

I need you to write a Bash script at `/home/user/filter.sh` that takes a single raw log file as an argument. The script must analyze the log, extract specific features, pass them to our scoring model, and exit with status code `0` if the log is clean, or exit `1` if it is anomalous (rejecting it).

Here are the details:
1. **The Data Format:** Each log file is a headerless CSV with the format: `timestamp,event_type,error_code,retries`.
2. **Feature Engineering:** You must compute three features from the log:
   - `Total Events`: The total number of lines in the file.
   - `Unique Errors`: The number of distinct, non-zero `error_code` values (ignore empty, `0`, or `None` values).
   - `Max Retries`: The highest integer value found in the `retries` column.
3. **The Model:** There is a compiled, stripped executable at `/app/anomaly_scorer`. I've lost the source code, but it acts as a Bayesian inference oracle. It expects exactly three positional arguments corresponding to the features above: `./anomaly_scorer <Total Events> <Unique Errors> <Max Retries>`. It prints a probability score between `0.00` and `1.00` to standard output.
4. **The Decision:** If the probability score output by the model is strictly greater than `0.75`, the script must consider the file anomalous and exit with status `1`. Otherwise, it should exit with `0`.

Your script should be robust, use only standard Bash, coreutils, and tools like `awk` or `sed`, and execute efficiently.