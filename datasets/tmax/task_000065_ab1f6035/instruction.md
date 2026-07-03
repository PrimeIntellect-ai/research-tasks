You are a data engineer tasked with building an ETL pipeline to process a unique optical telemetry feed. 

We have a video file located at `/app/sensor_feed.mp4` which contains encoded visual telemetry data. Alongside it, there is a large JSON Lines metadata file located at `/app/metadata.jsonl` containing synchronization timestamps.

Your objective is to build a data pipeline that performs the following steps:
1. **Video Streaming & Extraction**: Stream the video `/app/sensor_feed.mp4` frame-by-frame. For each frame, calculate the telemetry signal: the mean grayscale value (0-255) of the center 64x64 pixel region.
2. **Text & Metadata Processing**: Read the `/app/metadata.jsonl` file. Each line is a JSON object like `{"frame_index": 0, "timestamp": "2024-01-01T00:00:00Z"}`.
3. **Data Merging**: Join the extracted visual signal with the metadata based on the frame index. 
4. **Data Writing**: Output the merged data into a Parquet file at `/home/user/telemetry.parquet`. The schema must contain: `frame_index` (integer), `timestamp` (string), and `signal` (float).
5. **Logging**: Maintain a log file at `/home/user/pipeline.log`. Log the start of the process, progress updates (e.g., every 100 frames), and the completion status.

Requirements:
- You may use any programming language (Python, bash, etc.).
- The pipeline must handle the files efficiently (avoiding reading entire massive text files into memory at once where possible, though the provided test file may be small enough).
- The metric for success is the Mean Squared Error (MSE) of your extracted `signal` compared to our ground truth. 

Provide the commands and code to complete this pipeline. Ensure the final Parquet file is written exactly to `/home/user/telemetry.parquet`.