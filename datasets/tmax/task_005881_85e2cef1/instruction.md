You are a data engineer responsible for building an ETL pipeline that processes time-series data from legacy IoT sensors. These sensors output data in different character encodings, and your goal is to ingest this data, normalize it, compute a similarity metric between the sensor streams, and set up the orchestration for scheduling.

The system has provided two raw data files in `/home/user/data/`:
1. `/home/user/data/sensor_a.csv`: Contains readings from Sensor A. Due to a legacy French firmware, this file is encoded in **ISO-8859-1**.
2. `/home/user/data/sensor_b.csv`: Contains readings from Sensor B. Due to an older Windows CE export system, this file is encoded in **UTF-16LE** (without BOM).

Both CSV files have the same structure (comma-separated, no headers):
`timestamp,value,status_label`
- `timestamp`: Unix epoch integer (e.g., `1600000000`)
- `value`: Float representing the sensor reading
- `status_label`: String containing text (with non-ASCII characters).

Your task is to write a Go program that acts as the core of this ETL pipeline, and then set up its execution schedule.

**Requirements:**
1. **Go Program**: Create a Go module in `/home/user/etl/`. Write a program `main.go` that:
   - Reads both CSV files, correctly decoding them from their respective encodings (ISO-8859-1 and UTF-16LE) to standard UTF-8 strings.
   - Extracts the time-series points (`timestamp` and `value`).
   - Aligns the two time series by matching exactly identical timestamps (an inner join on `timestamp`).
   - Computes the **Euclidean Distance** between the `value` readings of Sensor A and Sensor B for the aligned timestamps. The formula is: `sqrt( sum( (A_i - B_i)^2 ) )` for all aligned pairs `i`.
   - Writes the result to a JSON file at `/home/user/output/metrics.json` with the exact structure:
     `{"distance": <float64>, "aligned_points": <integer>}`

2. **Orchestration & Scheduling**:
   - Create a bash script at `/home/user/run_pipeline.sh` that builds and executes your Go program. Ensure the script is executable.
   - We need to schedule this pipeline. Create a text file at `/home/user/pipeline.cron` that contains exactly one crontab line to execute `/home/user/run_pipeline.sh` every 15 minutes (e.g., at minutes 0, 15, 30, 45).

You may use standard Go libraries and `golang.org/x/text` for encodings.