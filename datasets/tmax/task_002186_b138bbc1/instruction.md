You are a Machine Learning Engineer preparing a robust training data pipeline for continuous spectroscopy data. You need to glue together several microservices, fix web server configurations, and implement the core statistical processing engine using standard shell tools.

### System Architecture & Environment
The environment has several services pre-installed and running (managed by supervisor or background processes):
1. **Sensor Simulator**: Running locally on TCP port `9001`. Upon connection, it continuously streams noisy spectral data. Each line is a single observation containing 100 comma-separated intensity values (e.g., `12.4,15.1,14.8,...`).
2. **Redis**: Running on `127.0.0.1:6379`.
3. **Feature API**: A simple Python Flask service running on `127.0.0.1:5000`. It exposes `GET /features`, which reads a JSON string from the Redis key `latest_stats` and returns it.
4. **Nginx**: Running on port `8080`, but its configuration is broken.

### Your Objectives

**1. Service Composition (Nginx)**
The web server must act as the unified entry point.
- Edit the Nginx configuration so that any request to `http://127.0.0.1:8080/api/data` is reverse-proxied to the Feature API at `http://127.0.0.1:5000/features`.
- Restart or reload Nginx to apply changes. 

**2. Bash Statistical Processor (`/home/user/pipeline.sh`)**
Write a Bash script that acts as the core data pipeline. It must use only Bash, `awk`, `sed`, `nc`, `redis-cli`, etc. (no Python or R). The script must perform the following exactly:
- **Ingest**: Read exactly 100 consecutive lines (spectra) from `127.0.0.1:9001`.
- **Signal Processing**: For each of the 100 spectra, apply a 3-point moving average filter to the intensities: $y'_i = (y_{i-1} + y_i + y_{i+1})/3$. For the boundaries ($i=1$ and $i=100$), use a 2-point average of the available points. After smoothing, extract the peak (maximum) intensity value for each spectrum. You will now have 100 peak values.
- **Bootstrapping (Confidence Intervals)**: Using `awk` and its random number generation, perform a bootstrap resampling (with replacement) of these 100 peak values to compute the 95% confidence interval for the **mean** peak value. Use exactly `B=500` bootstrap iterations. Find the lower (2.5th percentile) and upper (97.5th percentile) bounds of the resampled means.
- **Density Estimation**: Compute a histogram of the original 100 peak values. Find the exact minimum and maximum of the 100 peaks. Create exactly 5 equal-width bins spanning from this min to max. Count the number of peaks falling into each bin (values exactly on a boundary should go to the lower bin, except the absolute maximum which goes to the highest bin).
- **Export**: Construct a JSON payload with the results:
  ```json
  {
    "ci_lower": 45.21,
    "ci_upper": 48.95,
    "hist_counts": [12, 34, 28, 20, 6]
  }
  ```
- Write this JSON payload into Redis under the key `latest_stats` using `redis-cli`.

**Execution Constraints**:
- Your script `/home/user/pipeline.sh` should be executable and run successfully to populate the Redis key so the test suite can immediately evaluate the endpoint.
- You do not need to loop the script continuously; just run it once to process 100 lines and store the result.