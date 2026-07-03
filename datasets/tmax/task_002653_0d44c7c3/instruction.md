You are a data engineer tasked with building a robust ETL pipeline to process legacy radar tracking data. You have been provided with a video recording of a radar screen (`/app/radar_scan.mp4`) and a noisy metadata log (`/app/sensor_meta.txt`). 

Your goal is to extract the movement trajectory of the tracked object and schedule this pipeline.

Step 1: Frame Extraction
Use `ffmpeg` to extract the frames from `/app/radar_scan.mp4` at 10 frames per second. Save them as grayscale PGM (Portable GrayMap) images in `/home/user/frames/`.

Step 2: Metadata Parsing
The file `/app/sensor_meta.txt` contains messy logs. You must use Regular Expressions to extract valid log entries. A valid entry starts with `[VALID]`, followed by a timestamp in milliseconds (e.g., `T:1000`), and a sensor status of `ACTIVE`. 

Step 3: Trajectory Extraction (C++)
Write a C++ program (`/home/user/process_radar.cpp`) that:
1. Takes the parsed valid timestamps to identify which frames to process (e.g., `T:1000` corresponds to frame at 1.0 seconds, which is frame 10 if 1-indexed or 10 if 0-indexed depending on your ffmpeg output).
2. Reads the corresponding PGM frames.
3. Normalizes the pixel intensities of each frame to a standard scale (0.0 to 1.0).
4. Calculates the center of mass (x, y coordinates) of the normalized pixel intensities to find the tracked object (which appears as a bright white blob on a dark background).
5. Computes the Euclidean distance from the center of the frame (assuming the frame is perfectly square, e.g., if 100x100, the center is at 50.0, 50.0) to the calculated center of mass.
6. Outputs a CSV file at `/home/user/trajectory.csv` with the header: `timestamp_ms,x,y,distance_to_center`.

Step 4: Pipeline Automation
Create a bash script at `/home/user/etl_pipeline.sh` that executes Steps 1-3 sequentially. 
Finally, create a file `/home/user/cron_schedule.txt` containing the exact cron expression to run this bash script every 5 minutes, every day.

Constraints:
- The primary data processing logic must be written in C++17 or later. You may use standard libraries only.
- The output CSV must accurately track the object's distance from the center. Accuracy will be evaluated by calculating the Mean Squared Error (MSE) of your `distance_to_center` column against our ground truth.