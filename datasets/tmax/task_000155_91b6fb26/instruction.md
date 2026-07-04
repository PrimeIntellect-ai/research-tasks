You are a performance engineer tasked with debugging and optimizing a Python data processing pipeline located in `/home/user/pipeline/`.

The pipeline consists of a script `aggregator.py` that reads floating-point sensor values from `/home/user/pipeline/data.csv` and calculates their sum. 

Currently, the pipeline has three major issues:
1. **Environment/Configuration Misconfiguration**: The script takes an unusually long time to run. There is a misconfiguration in `/home/user/pipeline/config.ini` that dictates how the file is read. You must identify the bottleneck and fix the configuration so the script runs efficiently (the file should be processed in large chunks, not line-by-line or byte-by-byte).
2. **Corrupted Input Handling**: `data.csv` contains some corrupted entries (e.g., "ERR", "NaN", or random strings). The script currently crashes when encountering these. You need to modify `aggregator.py` to catch these errors gracefully. When a corrupted row is found, treat its value as `0.0`, and increment a `corrupted_count` variable.
3. **Precision Loss**: The dataset contains a mix of extremely large and extremely small floating-point numbers. The naive summation approach currently used in the script results in severe precision loss (floating-point catastrophic cancellation/absorption). You must track and fix this. 

**Your tasks:**
1. Fix `config.ini` so the script uses a `chunk_size` of `10000`.
2. Modify `aggregator.py` to handle corrupted data (skipping the crash, yielding `0.0`, and counting the errors).
3. Modify `aggregator.py` to calculate two values:
   - `naive_sum`: The sum calculated using standard Python addition (`+` or standard `sum()`) in the exact order the values appear in the file.
   - `precise_sum`: The mathematically correct sum avoiding precision loss, utilizing `math.fsum()`.
4. Run your modified script and save the final results to `/home/user/pipeline/result.json` exactly in this format:
   ```json
   {
       "naive_sum": <float>,
       "precise_sum": <float>,
       "corrupted_count": <int>
   }
   ```
5. **Regression Test Construction**: Create a regression test file at `/home/user/pipeline/test_precision.py`. It should contain a function `test_precision_recovery()` that uses `pytest` or standard `assert` to verify that `math.fsum` correctly sums the list `[0.1] * 10000 + [1e16] + [0.1] * 10000` to exactly `10000000000002000.0`, whereas standard `sum()` does not. 

Work strictly within `/home/user/pipeline/`. Ensure `result.json` and `test_precision.py` are present and correct when you finish.