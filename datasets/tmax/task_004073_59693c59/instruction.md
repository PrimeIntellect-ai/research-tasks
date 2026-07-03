You are an ML Engineer preparing an anomaly detection dataset from a traffic camera video. You need to process the video, perform vector math to detect visual anomalies, join the findings with external sensor data, and manage your disk space efficiently—all using standard Bash tools and command-line utilities.

We have a video artifact located at `/app/traffic.mp4`.
We also have a metadata file at `/app/sensor_data.csv` with the format: `timestamp_sec,sensor_id,ambient_temp`.

Your task is to write a complete Bash workflow (which you can execute to produce the final output) that does the following:

1. **Environment & Storage Preparation:**
   Create a working directory `/home/user/processing`. Make sure to handle the large number of frames carefully so you don't run out of disk space.

2. **Frame Extraction:**
   Extract frames from `/app/traffic.mp4` at exactly 1 frame per second (fps). The first frame corresponds to `timestamp_sec = 0`.

3. **Linear Algebra & Feature Engineering (in Bash/Awk):**
   For each extracted frame, calculate the average Red, Green, and Blue pixel values across the entire image. 
   *(Hint: You can scale the image down to 1x1 pixel using `ffmpeg` and output as raw RGB to get the average color, then read it with `od` or `hexdump`.)*
   Let this average color be the vector $\vec{v} = (R, G, B)$.
   Calculate the Euclidean distance between $\vec{v}$ and the baseline background vector $\vec{b} = (110, 115, 120)$.
   
4. **Data Filtering:**
   Identify all timestamps (in seconds) where the Euclidean distance is strictly greater than `35.0`. These are your visual anomalies.

5. **Multi-source Data Joining:**
   Join your visual anomalies with the `/app/sensor_data.csv` file on the `timestamp_sec` column.
   
6. **Output Generation:**
   Create a final CSV report at `/home/user/anomalies.csv` with the header `timestamp_sec,sensor_id,euclidean_distance`.
   The `euclidean_distance` must be rounded to exactly 2 decimal places. Sort the file numerically by `timestamp_sec`.

7. **Storage Management:**
   Once `/home/user/anomalies.csv` is generated, delete all extracted raw frames to free up disk space.

An automated grader will read your `/home/user/anomalies.csv` and compare it against the reference data. Because slight rounding differences can occur based on how image downscaling is implemented, the verification will be based on a quantitative metric: 
- The F1-score of the retrieved `timestamp_sec` must be $\geq 0.90$.
- The Mean Absolute Error (MAE) of the calculated distances for correctly identified timestamps must be $\leq 2.0$.