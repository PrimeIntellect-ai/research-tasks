You are an automation specialist tasked with building a mathematical data preparation pipeline for a meteorological modeling system. The input data arrives in a wide-format CSV, and you need to build a multi-step workflow to reshape, augment, validate, and sample the data for downstream training.

You may use Python, Bash, or any combination of standard Linux command-line tools to accomplish this.

**Input Data:**
A file exists at `/home/user/sensor_data.csv`. 
It contains daily readings for multiple stations in a wide format. 
Columns: `Date` (YYYY-MM-DD), `S1_T`, `S1_H`, `S2_T`, `S2_H`, `S3_T`, `S3_H`, `S4_T`, `S4_H`.
`_T` stands for Temperature and `_H` stands for Humidity. 

**Workflow Requirements:**

1. **Wide-Long Reshaping:**
   Transform the dataset into a long-format CSV with the exact columns: `Date`, `Station`, `Temperature`, `Humidity`.
   The `Station` column should contain the station prefix (e.g., `S1`, `S2`, `S3`, `S4`).

2. **Feature Extraction Transforms:**
   Add two new mathematical features to the long-format dataset:
   *   `THI`: A simplified Temperature-Humidity Index calculated as `Temperature + (0.5 * Humidity)`. Leave empty/NaN if either input is missing.
   *   `Temp_Rolling_3`: A 3-day rolling average of the `Temperature`, computed per station, ordered by `Date`. Use a minimum period of 1 (meaning the first day's average is just the first day's value, the second is the average of day 1 and 2, etc.).

3. **Validation Checkpoints (Quality Gate):**
   Evaluate each station's data quality. A station is considered **INVALID** and must be entirely dropped from the final dataset if it violates *either* of these rules:
   *   **Rule A:** Contains any `Temperature` reading `< -40.0` or `> 60.0`.
   *   **Rule B:** Has more than `5%` of its rows missing the `THI` value (due to missing temperature or humidity).
   Write the names of the valid stations (one per line, sorted alphabetically) to `/home/user/valid_stations.txt`.

4. **Data Sampling and Stratification:**
   Using *only the valid stations*, extract a stratified sample to build the final training set.
   *   Extract the month from the `Date` column (1 through 12).
   *   For each valid station, sample exactly **2 days per calendar month** (regardless of the year, though the input only spans one year).
   *   To ensure reproducibility, if using Python/pandas, use `.sample(n=2, random_state=42)` for each group (grouped by Station and Month).
   *   Save the resulting dataset to `/home/user/final_training_sample.csv`.
   *   The final CSV must contain the columns: `Date`, `Station`, `Temperature`, `Humidity`, `THI`, `Temp_Rolling_3`.
   *   Sort the final CSV by `Station` ascending, then `Date` ascending.

Execute this pipeline and ensure the output files (`/home/user/valid_stations.txt` and `/home/user/final_training_sample.csv`) are created exactly as specified.