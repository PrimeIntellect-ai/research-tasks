You are a data scientist tasked with cleaning a corrupted, real-time IoT sensor data stream. We have a multi-service pipeline set up in `/app/`. 

Our raw data stream contains temperature readings from an industrial sensor, but the network is unreliable. The stream suffers from:
1. Missing data points (gaps up to 5 seconds).
2. Out-of-order delivery (up to 3 seconds delayed).
3. Extreme noise/anomalies caused by sensor glitches (e.g., sudden spikes above 150°C or drops below -50°C).

Your objective is to write a processing script (in any language you choose, though Python or Bash/Awk are recommended) that reads this stream, cleans it, aggregates it, and forwards it to a downstream API.

System setup:
- A `startup.sh` script located at `/app/startup.sh` starts the background services. Run it before you begin.
- **Service 1 (Data Producer):** Listens on TCP port 9000 (`localhost:9000`). When you connect to it (e.g., via `nc localhost 9000`), it will stream CSV data indefinitely. 
  - Format: `timestamp,sensor_id,temperature` (e.g., `1700000000,S1,45.2`)
  - The stream emits approximately 1 reading per second, but has out-of-order rows and missing seconds.
- **Service 2 (Downstream Aggregator API):** A local HTTP server listening on port 8080. It accepts cleaned, aggregated data via `POST /submit`.

Pipeline Requirements:
1. **Validation Checkpoint:** Discard any raw readings where the temperature is `< -50.0` or `> 150.0`. 
2. **Sorting & Buffering:** Handle out-of-order arrivals. Sort the data logically by `timestamp`.
3. **Resampling & Gap-filling:** Resample the data to a strict 1-second frequency. If a timestamp is missing, use forward-filling (carry forward the last valid observed temperature) to fill the gap.
4. **Time-based Bucketing:** Aggregate the 1-second resampled data into **10-second tumbling windows**. A window starts at timestamps ending in `0` (e.g., `1700000000` to `1700000009`). 
5. **Quality Gate:** If a 10-second window cannot be aggregated because there were no valid readings to forward-fill from at the start of the window, drop the entire window.
6. **Forwarding:** Calculate the mean temperature for each 10-second window. Send an HTTP POST request to `http://localhost:8080/submit` with a JSON payload exactly in this format:
   `{"window_start": 1700000000, "avg_temp": 45.23}`

Create your solution in `/home/user/pipeline.sh` or `/home/user/pipeline.py`. Run it for at least 60 seconds of stream time so the aggregator API collects enough windows in its local storage (`/tmp/results.json`).