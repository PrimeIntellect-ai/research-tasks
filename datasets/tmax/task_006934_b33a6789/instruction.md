You are an ML engineer preparing training data from raw spectroscopy signals. 
You have raw data stored in `/home/user/raw_data/` as several CSV files (`data_1.csv`, `data_2.csv`, etc.). Each CSV file has a header `wavelength,intensity` and contains sequential measurements.

Your task is to create a reproducible data processing pipeline in Rust to extract features from these signals for a machine learning model.

Perform the following steps:
1. Create a new Rust project named `spectro_prep` in `/home/user/spectro_prep`.
2. Write a Rust program that reads all CSV files in `/home/user/raw_data/` (ending in `.csv`).
3. For each file, apply a moving average filter to the `intensity` values with a window size of 5. 
   - Specifically, `smoothed[i] = (intensity[i-2] + intensity[i-1] + intensity[i] + intensity[i+1] + intensity[i+2]) / 5.0`.
   - For indices `0, 1` and `N-2, N-1` (where N is the number of rows), set the `smoothed` value to `0.0`.
4. Find all local maxima in the smoothed signal. A local maximum occurs at index `i` if `smoothed[i] > smoothed[i-1]` and `smoothed[i] > smoothed[i+1]`. Do not check indices `0` or `N-1`.
5. Identify the wavelengths corresponding to the top 3 highest peaks (based on their smoothed intensity) in descending order of intensity. If a file has fewer than 3 peaks, fill the remaining values with `0.0`.
6. Output a final CSV file at `/home/user/training_data.csv` with the exact header: `filename,peak1_wl,peak2_wl,peak3_wl`.
   - `filename` should just be the base name of the file (e.g., `data_1.csv`).
   - Format the wavelengths to 1 decimal place (e.g., `150.0`).
   - The rows in the output CSV must be sorted alphabetically by `filename`.

Build and run your pipeline so that `/home/user/training_data.csv` is correctly generated.