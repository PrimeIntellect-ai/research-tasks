You are an automation specialist tasked with building a robust time series data ingestion and filtering pipeline. 

We rely on a proprietary, internally developed Python library called `fast_ts_parser` located at `/app/fast_ts_parser` for reading and extracting features from raw time series CSV files. However, we've noticed a severe issue: the pipeline occasionally drops critical time series records entirely. After some investigation, we suspect the bug is inside the `fast_ts_parser` package, specifically in how it handles multi-line CSV fields (e.g., descriptions containing embedded newlines) during parallel processing chunks.

Your objectives:
1. Debug and fix the `fast_ts_parser` package so that it correctly parses all rows without dropping those with embedded newlines. Ensure that the package's feature extraction transforms and distance computations work as intended.
2. Build a data sanitization script `/home/user/sanitize_ts.py` that uses the fixed `fast_ts_parser` library. The script must take an input CSV directory of time series data and an output CSV directory.
   - Command line signature: `python3 /home/user/sanitize_ts.py --input-dir <input_dir> --output-dir <output_dir> --reference <reference_csv>`
3. The script must filter out "anomalous" time series. A time series is considered anomalous (evil) if its extracted features exhibit a Dynamic Time Warping (DTW) distance greater than 50.0 compared to the reference time series provided, or if the time series contains invalid string characters in its numeric columns. 
4. Valid time series must be preserved and written to the output directory exactly as they appeared, maintaining the original file names.

You will be evaluated against a hidden dataset of clean and malicious (evil) time series files to ensure your filter rejects 100% of malicious files while preserving 100% of the clean ones.