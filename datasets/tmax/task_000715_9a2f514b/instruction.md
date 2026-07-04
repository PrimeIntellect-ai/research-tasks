You are acting as an AI assistant for a researcher organizing datasets from a recent lab experiment. The researcher has video footage of the experiment and an independent log of sensor readings, and needs to combine these datasets to model the relationship between the visual events and the sensor data.

Here is your multi-stage assignment:

**Phase 1: Video Data Extraction**
1. You have a video file located at `/app/experiment_video.mp4` (25 frames per second).
2. Install any necessary dependencies (e.g., ffmpeg, python packages) to process this video.
3. Write a script to calculate the average grayscale pixel intensity for every single frame in the video.
4. Save the results to `/home/user/video_stats.csv` with the headers: `frame_index,timestamp_ms,avg_brightness`. The `timestamp_ms` should be calculated as `frame_index * 40` (since it's 25 fps). Format `avg_brightness` to two decimal places (e.g., `128.50`).

**Phase 2: Data Joining in C**
1. The researcher has provided sensor data at `/app/sensor_data.csv` with the headers: `timestamp_ms,sensor_value`.
2. Write a C program at `/home/user/join_stats.c` that takes two file paths as command-line arguments: the video stats CSV and the sensor data CSV.
   Usage: `./join_stats <video_csv> <sensor_csv>`
3. The C program must perform an inner join on the `timestamp_ms` column. For every exact match of `timestamp_ms` in both files, print a joined row to standard output in the format: `timestamp_ms,avg_brightness,sensor_value`.
4. If there are multiple identical timestamps in either file, join only the first occurrence encountered in each file. If a timestamp exists in one file but not the other, ignore it. Print the joined rows ordered by how they appear in the `<video_csv>`.
5. Compile your C program to `/home/user/join_stats`. Your program must be exceptionally robust. It will be aggressively tested against an existing, compiled reference binary (oracle) provided by the researcher. Your output must be bit-exact equivalent to the oracle for *any* valid input files.

**Phase 3: Statistical Modeling**
1. Run your compiled `./join_stats` program on `/home/user/video_stats.csv` and `/app/sensor_data.csv` and redirect the output to `/home/user/joined_dataset.csv`. (Ensure you manually add the header `timestamp_ms,avg_brightness,sensor_value` to the top of `/home/user/joined_dataset.csv`).
2. Write a Python script to train an Ordinary Least Squares (OLS) Linear Regression model predicting `sensor_value` (dependent variable) using `avg_brightness` (independent variable).
3. Save the calculated slope (coefficient for `avg_brightness`) to `/home/user/model_result.txt`, rounded to exactly 4 decimal places.