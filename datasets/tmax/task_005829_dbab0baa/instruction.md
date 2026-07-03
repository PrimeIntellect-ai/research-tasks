You are assisting a researcher in organizing and preprocessing a batch of mathematical sensor datasets. The raw datasets are stored as CSV files, but they contain missing values and extreme outliers. After cleaning the data, you need to apply a simple linear model to the features and evaluate the numerical results. 

Your task is to create a Bash pipeline script at `/home/user/process_sensors.sh` that performs the following steps. You must make the script executable and run it so the final outputs are generated.

1. **Data Organization:**
   There is a directory `/home/user/raw_sensors/` containing multiple CSV files (e.g., `sensor_A.csv`, `sensor_B.csv`). Each file has a header `id,f1,f2,f3` and several rows of data.
   Create a directory `/home/user/processed_sensors/`.

2. **Missing Value & Outlier Handling:**
   For each CSV file, read the data and perform the following cleaning steps on features `f1`, `f2`, and `f3`:
   - Replace any missing values (represented by the string `NA`) with `0.0`.
   - Clip extreme outliers: any value greater than `50.0` must be replaced with `50.0`, and any value less than `-50.0` must be replaced with `-50.0`.
   - Save the cleaned tabular data into `/home/user/processed_sensors/` keeping the exact same filenames and headers.

3. **Model Reconstruction & Inference:**
   There is a file `/home/user/model_weights.txt` containing a single line with three comma-separated floating-point numbers corresponding to weights for `f1`, `f2`, and `f3` (e.g., `0.5,-0.2,1.5`).
   Using Bash tools (like `awk`), reconstruct this linear model: `prediction = (w1 * f1) + (w2 * f2) + (w3 * f3)`.
   Apply this model to all the cleaned data. 
   Concatenate the results into a single file at `/home/user/all_predictions.csv` with the header `id,prediction` (sort by `id` numerically in ascending order).

4. **Numerical Accuracy & Aggregation:**
   Calculate the sum of all the `prediction` values in `/home/user/all_predictions.csv`. 
   Save this single numerical value (formatted to 2 decimal places) into `/home/user/prediction_sum.txt`.

5. **Storage Management:**
   Compress the `/home/user/processed_sensors/` directory into a tarball at `/home/user/clean_data_archive.tar.gz`.

Ensure your Bash script handles the math accurately. Once you have written `/home/user/process_sensors.sh`, execute it to generate the final files.