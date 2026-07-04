You are tasked with modernizing a legacy data processing pipeline for a sensor network. 

Currently, we have a compiled, stripped C++ binary located at `/app/legacy_processor`. This tool takes a messy, wide-format CSV containing sensor readings with missing data, performs some proprietary data cleaning (which involves reshaping and interpolation), and outputs a clean, long-format CSV. However, the legacy tool is single-threaded and too slow for our growing data volumes.

Your objective is to reverse-engineer the exact data transformation logic of `/app/legacy_processor` and implement a fast, parallelized version in Python.

**Input CSV Format:**
- Column 1: `timestamp` (integer, strictly increasing)
- Columns 2 to N: `sensor_A`, `sensor_B`, etc. (float values, occasionally missing represented as empty strings or `NaN`)

**Requirements for your Python script:**
1. **Location & Execution:** Must be saved at `/home/user/fast_processor.py`.
2. **CLI Interface:** Must accept exactly three arguments: 
   `python /home/user/fast_processor.py <input_csv_path> <output_csv_path> --workers <num_workers>`
3. **Data Transformations (Reverse Engineered):** You must determine exactly how the legacy binary processes the data. Experiment with `/app/legacy_processor <input.csv> <output.csv>` to observe its behavior. It generally performs wide-to-long format reshaping, missing value imputation (interpolation), and sorts the output, but you must match its rounding, sorting, and interpolation rules *exactly*.
4. **Parallelism:** Your script must utilize the `--workers` argument to perform the data processing in parallel (e.g., using Python's `multiprocessing` or `concurrent.futures` modules to process different chunks of the data or different sensors concurrently).
5. **Bit-Exact Output:** Your script's output CSV must be perfectly identical (bit-exact) to the output produced by the legacy binary for any given valid input CSV.

You can use standard data science libraries like `pandas` and `numpy` which are installed in the environment. Create some dummy CSV files to test and compare your outputs against `/app/legacy_processor` until you achieve perfect parity.