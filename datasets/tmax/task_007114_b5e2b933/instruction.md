You are a data scientist cleaning a dataset of sensor locations. 
There is a file at `/home/user/sensor_data.csv` containing timestamps and sensor coordinates in a wide format.

The columns are:
`timestamp, d1_x, d1_y, d2_x, d2_y, d3_x, d3_y`

Your task is to write a Python script that processes this data to produce a summary of the maximum distance recorded per device in each 1-hour time bucket. 

Specifically, you must:
1. Reshape the data from wide to long format so that each row represents a single device's reading at a specific timestamp. The columns conceptually should be `timestamp`, `device_id`, `x`, `y`. The `device_id` should be just the string prefix (e.g., `d1`, `d2`, `d3`).
2. Bucket the timestamps into 1-hour intervals (e.g., `2023-10-01T10:15:00Z` becomes `2023-10-01T10:00:00Z`).
3. Calculate the Euclidean distance of each reading's `(x, y)` coordinates from the origin `(0.0, 0.0)`.
4. Stratify/group the data by `bucketed_hour` and `device_id`, and find the maximum distance for each group.
5. Save the results to `/home/user/cleaned_max_distances.csv` with exactly these columns: `bucketed_hour,device_id,max_distance`.
6. Round `max_distance` to exactly 2 decimal places (e.g., `2.83`, `5.00`).
7. Sort the output CSV ascendingly first by `bucketed_hour`, then by `device_id`.

Ensure your Python script runs and creates the output file successfully.