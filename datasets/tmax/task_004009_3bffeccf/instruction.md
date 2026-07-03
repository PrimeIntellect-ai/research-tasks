You are tasked with building a streaming data processing pipeline for customer service call analysis. You need to combine audio transcription, pipeline scheduling, C++ text processing, rolling statistics, anomaly detection, and a web API.

Here are the requirements:

1. **Audio Transcription:**
   You have an audio recording of a customer call located at `/app/call_recording.wav`. Transcribe this audio file to text. Extract the words and save them sequentially into a CSV file at `/home/user/transcript.csv` with the format `index,word` (where index starts at 0 for the first word). Strip all punctuation and convert words to lowercase.

2. **C++ Anomaly & Rolling Stats Server:**
   Write a C++ program in `/home/user/analyzer.cpp` and compile it to `/home/user/analyzer`. This program must:
   * Continually read (or poll) `/home/user/stream.csv`, which will receive streamed data in the same `index,word` format.
   * Maintain a rolling average of the string length of the **last 10 words** received. (If fewer than 10 words have been received, average over the available words).
   * Perform anomaly detection: An "anomaly" is triggered whenever the rolling average of word lengths strictly exceeds `6.0`. Keep a persistent count of the total number of anomalies detected.
   * Run an HTTP server listening on `127.0.0.1:8080`.
   * Expose a `GET /metrics` endpoint that returns a JSON response: `{"rolling_avg": <current_rolling_average>, "anomalies": <total_anomalies>}`. The `rolling_avg` should be a float rounded to 2 decimal places.

3. **Pipeline Scheduling (Cron):**
   Create a bash script at `/home/user/feed.sh` that simulates streaming data. Every time the script runs, it should read the next 10 lines from `/home/user/transcript.csv` that haven't been processed yet, and append them to `/home/user/stream.csv`.
   * You will need to maintain a state file (e.g., `/home/user/offset.txt`) to remember the last processed index.
   * Schedule this script using `cron` to run every minute (`* * * * *`). 

4. **Execution:**
   * Start the `cron` daemon.
   * Compile and start your C++ server in the background.
   * Wait a few minutes for the cron job to feed enough data into `stream.csv`, or manually execute `/home/user/feed.sh` a few times to populate `stream.csv`.
   * Ensure the server correctly updates its state and serves the JSON endpoint.

Write robust code, handle file I/O properly in C++, and ensure your HTTP server gracefully handles concurrent or repeated requests. Do not use external libraries for the C++ HTTP server if possible; basic socket programming or a single-header library available via `apt` (like `nlohmann-json3-dev` and basic sockets) is preferred.