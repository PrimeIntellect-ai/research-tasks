You are tasked with investigating and fixing a severe memory leak in our data processing service, located at `/home/user/service`. The service calculates the running variance of a high-frequency data stream to detect anomalies. 

However, the previous engineer left things in a broken state:
1. **Deleted Configuration Recovery:** The critical configuration file containing the anomaly threshold was accidentally deleted. Fortunately, a background monitoring daemon is still holding the file open. You must recover the contents of this deleted file and save it to `/home/user/recovered_threshold.txt`.
2. **Dependency Resolution:** The service's Python environment is broken. The `/home/user/service/requirements.txt` file contains conflicting dependencies. You must resolve the conflict so that `pip install -r requirements.txt` succeeds without errors, allowing you to run the service.
3. **Formula Correction & Memory Leak Fix:** The main script, `/home/user/service/analyzer.py`, processes `input_data.csv` line by line. It calculates the running variance, but it does so by appending every single value to a list, causing a massive memory leak (O(N) memory). Furthermore, the formula used for variance is numerically unstable and slightly incorrect for a population variance. 
   You must rewrite the `update_variance` function in `analyzer.py` to:
   - Use an O(1) memory algorithm (e.g., Welford's online algorithm or running sum/sum of squares) to compute the running population variance.
   - Stop storing historical data points in a list.
4. **Data Transformation & Reporting:** Once fixed, run `python /home/user/service/analyzer.py` to process `/home/user/service/input_data.csv`. It will output `output_fixed.csv`.

Finally, create a JSON report at `/home/user/resolution.json` with the following structure:
```json
{
  "recovered_threshold": <float value recovered from the deleted file>,
  "final_variance": <float value of the very last variance computed in output_fixed.csv>
}
```

Constraints:
- You may use any tools available in the standard Linux terminal.
- The `analyzer.py` must run with less than 50MB of memory overhead.
- Do not change the CLI arguments or standard output format of `analyzer.py`.