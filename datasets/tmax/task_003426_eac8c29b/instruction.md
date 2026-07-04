You are a data engineer tasked with building an ETL pipeline to process a noisy video feed from an industrial sensor. 

A video artifact is located at `/app/sensor_feed.mp4`. This video is a 30 FPS recording of a physical status indicator. The brightness of the indicator corresponds to the temperature of a machine. Unfortunately, the video feed suffers from camera flashes (sudden extreme brightness) and dropped frames (represented by completely black frames).

Your objective is to build a data processing pipeline that extracts the underlying temperature signal as a clean time series.

Please create a pipeline with the following steps:
1. **Extraction**: Process `/app/sensor_feed.mp4` to extract the average grayscale pixel intensity (0-255) for every frame. The frame index should start at 0.
2. **Anomaly Detection & Cleaning**: The raw time series will contain anomalies:
   - Flashes: Any frame where the average intensity is > 200.
   - Dropped frames: Any frame where the average intensity is < 10.
3. **Imputation**: Replace the anomalous frame values using linear interpolation based on the nearest valid preceding and succeeding frames.
4. **Orchestration**: Create an executable bash script at `/home/user/run_etl.sh` that takes the input video path as its first argument, runs your extraction and cleaning scripts (you may write these in Python, Ruby, or any standard tool), and produces the final output.
5. **Output**: The final step of the pipeline must generate a CSV file at `/home/user/cleaned_timeseries.csv` with exactly two columns: `frame` and `value` (the cleaned intensity, rounded to 2 decimal places).

To complete the task, build your scripts and execute `/home/user/run_etl.sh /app/sensor_feed.mp4`. 

Note: Your output will be evaluated against a hidden ground-truth time series using Mean Squared Error (MSE). You must achieve an MSE of less than 5.0 to pass.