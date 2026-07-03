You are an automation specialist tasked with building a multi-language pipeline to monitor industrial manufacturing equipment. We have a surveillance feed from the factory floor, and we need to automatically detect mechanical anomalies (e.g., sudden stutters, sudden lighting changes, or conveyor jams) using video processing and rolling statistics.

You must create an automated workflow that does the following:

1. **Video Ingestion:** Process the manufacturing surveillance video located at `/app/manufacturing_feed.mp4`.
2. **Frame Processing:** Extract frames at exactly 5 frames per second (FPS). You may use `ffmpeg` for this.
3. **Distance/Similarity Computation:** Write a script (in Python, C++, or Node.js) to compute the Mean Squared Error (MSE) of pixel intensities between consecutive extracted frames. 
4. **Rolling Statistics & Changepoint Detection:** Write a separate script (in a different language than step 3, e.g., if you used Python for MSE, use Perl, Ruby, or Bash/Awk for this step) that reads the frame-to-frame MSE values. It must compute a rolling moving average of the MSE values over a window of exactly 10 frames. Identify "anomalies" as any frame where the raw MSE exceeds the rolling average by more than 3 standard deviations.
5. **Data Validation & Formatting:** Validate that the output strictly conforms to a JSON array of timestamps (in seconds, rounded to 1 decimal place) where these anomalies occur. 

Save the final validated JSON array of anomaly timestamps to `/home/user/anomaly_timestamps.json`. 

Example output format for `/home/user/anomaly_timestamps.json`:
```json
[
  12.4,
  34.2,
  55.0
]
```

Your pipeline must be fully automated, executable via a single master shell script (`/home/user/run_pipeline.sh`), and must accurately detect the physical anomalies present in the video.