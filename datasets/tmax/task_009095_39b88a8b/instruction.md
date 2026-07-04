You are tasked with building a streaming configuration anomaly detection tool in C++. We have a configuration manager that tracks continuous numeric changes to service configurations (like connection pool limits, timeouts). 

We want to read a stream of configuration changes, compute rolling statistics per service, perform stratified sampling to reduce log volume, and normalize the metrics (compute z-scores) to detect drifts.

Create a C++ program at `/home/user/config_tracker.cpp`. This program must:
1. Read a CSV from standard input.
2. The input CSV has a header and lines in the format: `timestamp,service_name,metric_name,metric_value` (where `metric_value` is a double).
3. **Rolling Statistics**: Maintain a rolling window of the last `N=3` values for each `service_name`. The window must be updated with *every* incoming record for that service.
4. **Stratified Sampling**: For each `service_name`, track the number of updates received. You should only process and output an anomaly report for **even-numbered updates** for that service (i.e., the 2nd, 4th, 6th... appearance). The skipped records still update the rolling window.
5. **Normalization (Z-Score)**: When a record is sampled (emitted), compute its z-score based on the *current* rolling window of that service (which includes the current record). 
    * Mean ($\mu$) is the average of the items in the window.
    * Standard Deviation ($\sigma$) is the **population** standard deviation of the window: $\sigma = \sqrt{ \frac{\sum (x_i - \mu)^2}{N} }$ where $N$ is the current number of elements in the window (1, 2, or 3).
    * If $\sigma == 0$, the z-score should be exactly `0.0000`.
    * Z-score = $\frac{x - \mu}{\sigma}$

**Output Format**:
For every sampled record, print a line to standard output (no spaces after commas):
`service_name,timestamp,metric_value,rolling_mean,rolling_stddev,z_score`

Requirements for formatting floats in the output: print `metric_value`, `rolling_mean`, `rolling_stddev`, and `z_score` to exactly 4 decimal places using standard fixed precision (e.g. `std::fixed` and `std::setprecision(4)`).

Compile your code into `/home/user/config_tracker` using:
`g++ -std=c++17 -O3 /home/user/config_tracker.cpp -o /home/user/config_tracker`

Once compiled, test it on `/home/user/config_updates.csv`. Save the standard output of your compiled program to `/home/user/tracker_output.csv`.