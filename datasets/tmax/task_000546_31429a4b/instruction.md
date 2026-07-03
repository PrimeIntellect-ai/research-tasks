You are a localization engineer analyzing telemetry from a global translation API to identify performance patterns across different languages. The telemetry data is extremely large, so you need to process it efficiently.

You have a large CSV file located at `/home/user/translation_telemetry.csv` containing time-series data of translation requests.
The CSV has the following columns: `timestamp, language_code, latency_ms, words_translated`.
Timestamps are ISO 8601 strings covering a 24-hour period (e.g., `2023-10-01T00:00:00Z`).

Your task is to write a Python script `/home/user/analyze_telemetry.py` that does the following:

1. **Large-file streaming & Validation Quality Gate**: 
   Read the CSV file in a streaming fashion (e.g., using generators or chunking) to minimize memory usage. Implement a validation gate to filter out invalid rows. A row is invalid if `latency_ms <= 0`, `words_translated <= 0`, or `language_code` does not match the format `xx-XX` (two lowercase letters, hyphen, two uppercase letters).
   Count the number of invalid rows and write this integer to a text file `/home/user/invalid_count.txt`.

2. **Feature Extraction (Time Series Aggregation)**:
   For valid rows, aggregate the `latency_ms` into hourly bins for each language. Calculate the average latency for each hour (0 to 23). If a language has no valid requests in a specific hour, use `0.0` as the average for that hour. Sort the hours chronologically. You should end up with a 24-element list/vector of average latencies for each valid language.

3. **Distance Computation**:
   Using `es-ES` as the baseline language, compute the Euclidean distance between the 24-hour latency vector of `es-ES` and the latency vectors of all other languages. 

4. **Parallel Data Processing**:
   Use Python's `multiprocessing` module (e.g., `Pool`) to compute these Euclidean distances in parallel.

5. **Output**:
   Save the distances as a JSON file at `/home/user/distances.json`. The keys should be the language codes (excluding `es-ES`), and the values should be the Euclidean distance rounded to 4 decimal places.

Run your script to produce the output files.