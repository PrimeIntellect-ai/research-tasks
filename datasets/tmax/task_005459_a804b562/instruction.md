You are a data engineer tasked with building an ETL pipeline to analyze a monitoring video and serve the results via an API. All data processing must be written in Bash (using coreutils, awk, sed, standard CLI tools, and ffmpeg).

We have a video file located at `/app/monitoring.mp4`. Some frames in the video have been corrupted (resulting in complete blackness, i.e., average luminance of exactly 0) and there are occasional sudden flashes (anomalies).

Your pipeline must perform the following steps:
1. **Extract Metrics**: Use `ffmpeg`'s `signalstats` filter to analyze `/app/monitoring.mp4`. Extract the frame number (`n`) and the average luminance (`YAVG`) for every frame. 
2. **Imputation**: Clean the data. Any frame where the `YAVG` is exactly `0` or `0.0` is considered corrupted. Impute the `YAVG` of these corrupted frames by calculating the arithmetic mean of the `YAVG` of the immediately preceding valid frame and the immediately following valid frame. (Assume the first and last frames are never corrupted).
3. **Changepoint Detection**: Compute the absolute difference in the imputed `YAVG` between each frame and its previous frame. A changepoint (anomaly) is defined as any frame where this absolute difference is strictly greater than `50.0`.
4. **Data Aggregation**: Save the detected anomalies to a CSV file at `/home/user/anomalies.csv` with the format `frame_number,yavg_difference` (e.g., `45,127.5`). Do not include a header.
5. **Data Serving**: Build and start a simple HTTP server using Bash (`nc`, `socat`, or similar) that listens on `127.0.0.1:8080`. When the server receives an HTTP `GET /anomalies` request, it must respond with a valid `HTTP/1.1 200 OK` header followed by the exact contents of the `/home/user/anomalies.csv` file. The server must continue running and accept multiple requests.

Ensure your script is robust and correctly handles the pipeline end-to-end.