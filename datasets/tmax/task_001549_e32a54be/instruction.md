You are a data scientist working on an automated Bash pipeline to process observational sensor data, perform spectral analysis, and validate the numerical stability of your model's inputs. 

Your task is to create a Bash script `/home/user/run_analysis.sh` that performs the following steps:

1. **Observational Data Reshaping**
   You are provided with raw observational data in `/home/user/raw_sensor.dat`. The data is formatted as a single line of space-separated pairs in the format `time_value` (e.g., `0.00_1.23 0.01_1.45 0.02_1.10`). 
   Your Bash script must parse this file and convert it into a standard CSV file at `/home/user/clean_data.csv`. The CSV must have a header `time,value` followed by the comma-separated data rows.

2. **Spectral Analysis**
   You have been provided with a Python tool `/home/user/get_freq.py` that reads a CSV (with `time,value` headers), performs a Fast Fourier Transform (FFT) while ignoring the DC component (0 Hz), and prints the dominant frequency to stdout (formatted to 2 decimal places).
   Your Bash script should execute this Python script on `/home/user/clean_data.csv` and capture the resulting frequency.

3. **Reference Dataset Comparison**
   Read the reference frequency from `/home/user/reference.txt`. If the absolute difference between your calculated clean frequency and the reference frequency is less than `0.5`, the script should record the result as `MATCH`. Otherwise, record `MISMATCH`. (You can use `awk` or `bc` in Bash for the float comparison).

4. **Numerical Stability Testing**
   To ensure the dominant frequency extraction is stable against calibration offsets, use standard Linux text processing tools (like `awk`) to read `/home/user/clean_data.csv` and create `/home/user/noisy_data.csv`.
   In the noisy dataset, keep the header identical, but add exactly `0.05` to every value in the `value` column. The `time` column must remain unchanged.
   Run `/home/user/get_freq.py` on `/home/user/noisy_data.csv` to get the noisy frequency. If the noisy frequency is exactly equal to the clean frequency, the stability is `YES`, otherwise `NO`.

5. **Reporting**
   Your Bash script must generate a final report at `/home/user/analysis_report.txt` with exactly the following format:
   ```
   DATA_POINTS: <number of data rows in clean_data.csv, excluding the header>
   CLEAN_FREQ: <dominant frequency of clean data>
   REF_COMPARISON: <MATCH or MISMATCH>
   NOISY_FREQ: <dominant frequency of noisy data>
   STABLE: <YES or NO>
   ```

Make sure `/home/user/run_analysis.sh` is executable and run it to produce `/home/user/analysis_report.txt`. Do not modify the provided Python script.