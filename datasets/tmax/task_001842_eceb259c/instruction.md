You are tasked with fixing a broken configuration management pipeline. Our ETL job that records configuration state changes has been experiencing network timeouts, causing it to retry and produce duplicate time-series records.

We have a video recording of the deployment dashboard (`/app/deploy_dashboard.mp4`) covering a 60-second window (at 30 frames per second). The dashboard has a "Retry Deploy" warning indicator. The indicator is a red square in the top-left corner of the video (specifically, the 10x10 pixel region from x=0 to x=9, y=0 to y=9). When a retry is triggered, this region becomes solid red (RGB roughly 255, 0, 0). 

We also have a raw JSONL log file of the configuration events at `/app/data/config_events.jsonl`. Each line contains:
- `timestamp`: Float representing seconds from the start of the recording (0.0 to 60.0)
- `service_id`: String identifier
- `config_hash`: String hash of the configuration state
- `payload_size`: Integer size of the config payload in bytes

Your objective is to write a Python pipeline to clean this data and extract a specific time-series feature:
1. Extract the frames from `/app/deploy_dashboard.mp4` to determine the exact time windows when the ETL job was in "retry" mode. A second $S$ (from 0 to 59) is considered a "retry second" if *any* frame within that second (e.g., frames $30 \times S$ to $30 \times S + 29$) has the red indicator active (Average Red > 200, Green < 50, Blue < 50 in the top-left 10x10 pixels).
2. Stream and process the large `/app/data/config_events.jsonl` file. 
3. Deduplicate the records: If an event falls within a "retry second" AND its `config_hash` for the same `service_id` has already been seen in the log prior to this event, it is a duplicate created by the retry. Drop these duplicates.
4. From the cleaned, deduplicated events, perform a feature extraction transform: calculate the 5-second rolling sum of `payload_size` for all events across all services. Specifically, for each integer second $T$ from 0 to 59, sum the `payload_size` of all deduplicated events that occurred in the time window $(T-4, T]$ (i.e., strictly greater than $T-4$ and less than or equal to $T$). If a window has no events, the sum is 0.
5. Save this final time series to `/home/user/rolling_metrics.csv` with exactly two columns: `second` (integer, 0 to 59) and `rolling_size` (integer).

Ensure your script is robust and uses Python for the data processing.