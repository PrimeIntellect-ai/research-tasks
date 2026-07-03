You are an automation specialist tasked with creating a robust data ingestion pipeline for IoT sensor logs. The system must process files containing time-series data, filter out anomalous or adversarial records, and accept clean data.

Your task has two main phases:

**Phase 1: Fix and Install the Vendored Dependency**
We rely on a local package for fast time-series distance calculations, located at `/app/vendored/ts_distance/`. 
However, the package was recently modified and currently fails to install due to a configuration error. 
1. Identify and fix the perturbation in the package's build configuration.
2. Install the package in the environment. It provides a crucial function: `from ts_distance import compute_dtw`.

**Phase 2: Build the Data Filter**
Write a Python script at `/home/user/filter.py` that takes a single file path as a command-line argument. The script must determine if the file is "clean" (exit code 0) or "evil/invalid" (exit code 1).

The input files are binary files containing JSON text, but they have some quirks:
1. **Character Encoding**: Files may be encoded in either `UTF-8` or `UTF-16-LE`. Your script must dynamically detect and decode the file contents properly to parse the JSON.
2. **Data Extraction & Imputation**: The JSON contains a dictionary with a key `"sensor_readings"`, which is a list of numeric values and `null`s. You must impute any `null` values using strict linear interpolation between the nearest valid numbers. (Assume the first and last values are never `null`).
3. **Hash-Based Deduplication**: After imputation, convert the list of floats to a comma-separated string with exactly one decimal place (e.g., `"1.0,2.5,3.0"`). Compute the SHA-256 hex digest of this string. If the hash matches `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (a known malicious signature), reject the file.
4. **Distance Computation**: Use the installed `ts_distance.compute_dtw(seq1, seq2)` function to calculate the distance between your imputed sequence and the ideal baseline sequence: `[0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]`. 
5. **Acceptance Criteria**: If the file decodes successfully, the hash is not the malicious signature, and the DTW distance to the baseline is less than `15.0`, the script must terminate with exit code `0` (accept). Otherwise, or if any parsing errors occur, it must terminate with exit code `1` (reject).

Test your script against the files located in `/app/data/` to ensure it works properly before finalizing.