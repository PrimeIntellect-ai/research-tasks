You are a data scientist tasked with cleaning and analyzing sensor telemetry data from a fleet of delivery vehicles. The raw data has been dumped into a wide-format CSV file, but it needs to be restructured, enriched with windowed aggregations, and stratified for a downstream machine learning model.

The raw data is located at `/home/user/raw_fleet_data.csv`.

Your goal is to write a script (using Python, R, or Bash) that performs the following pipeline:

1. **Wide-to-Long Format Reshaping**: 
   The input CSV has columns like `timestamp`, `V1_speed`, `V1_temp`, `V2_speed`, `V2_temp`, etc. 
   You must reshape this data into a long format with exactly these columns: `timestamp`, `vehicle_id`, `speed`, `temp`. 
   (For example, `V1_speed` and `V1_temp` for a given timestamp should become a row where `vehicle_id` is `V1`).

2. **Windowed Aggregation**:
   Calculate a moving average of the `speed` column for each `vehicle_id` over a **3-row rolling window**, ordered chronologically by `timestamp`. 
   - Name this new column `rolling_speed_avg`.
   - Use a minimum window period of 1 (meaning the first row's rolling average is just its own speed, the second row's is the average of the first two, and the third is the average of the first three).
   - Round the `rolling_speed_avg` to exactly 2 decimal places.

3. **Stratified Sampling**:
   We only want to train the model on periods of high thermal stress. Group the reshaped data by `vehicle_id` and filter the dataset to keep **only the 2 rows with the highest `temp`** for each vehicle. (If there is a tie in temperature, break the tie by keeping the later `timestamp`).

4. **Output Specifications**:
   Save the final dataset to `/home/user/processed_fleet.csv`.
   - The CSV must have headers: `timestamp,vehicle_id,speed,temp,rolling_speed_avg`
   - The rows must be sorted by `vehicle_id` in ascending alphabetical order, and then by `timestamp` in ascending chronological order.

Please write and execute the code to generate `/home/user/processed_fleet.csv`.