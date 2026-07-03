You are a data engineer building an ETL pipeline to process traffic camera feeds and telemetry data. Your goal is to extract features from a video, join them with telemetry logs, and implement a data sanitiser in Bash to filter out anomalous readings based on a pre-trained linear model.

Here are the requirements for the task:

1. **Video Feature Extraction**:
   A surveillance video is located at `/app/traffic.mp4`. Extract the frames at a rate of 1 frame per second (starting at 00:00:00). For each extracted frame, calculate the average Red, Green, and Blue (RGB) pixel values. You may use `ffmpeg` or `imagemagick` for this.

2. **Multi-source Data Joining**:
   A telemetry log is provided at `/app/telemetry.csv`. It contains the following columns: `frame_index,speed,temperature`. 
   Join your extracted video features with the telemetry log on `frame_index` (the first frame is index 1, the second is 2, etc.).

3. **Model Architecture Reconstruction**:
   You have been given the weights of a simple linear anomaly detection model in `/app/model_weights.txt`. The model computes an anomaly score using the formula:
   `Score = (W_R * R_mean) + (W_G * G_mean) + (W_B * B_mean) + (W_speed * speed) + bias`
   If the `Score > 0`, the data point is considered an anomaly (an "evil" row) and must be filtered out.

4. **Adversarial Filter Creation**:
   Write a Bash script at `/home/user/filter_data.sh` that takes a single argument (the path to a CSV file containing joined data with columns `frame_index,R_mean,G_mean,B_mean,speed,temperature` without a header) and outputs the sanitized data (only the "clean" rows where `Score <= 0`) to standard output.
   
   To ensure your script is robust, we have provided two corpora of CSV files:
   - `/app/corpora/clean/`: Contains files with only clean data. Your script must preserve 100% of these rows.
   - `/app/corpora/evil/`: Contains files with anomalous data. Your script must reject 100% of these rows.

5. **Final Integration**:
   Run your pipeline on the `/app/traffic.mp4` video and `/app/telemetry.csv`. Pass the joined data through your `/home/user/filter_data.sh` script, and save the final sanitized output to `/home/user/final_output.csv`.

Ensure your `/home/user/filter_data.sh` script is executable and strictly outputs the preserved rows in the same CSV format (comma-separated, no header).