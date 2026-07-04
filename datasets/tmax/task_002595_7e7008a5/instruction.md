You are a Machine Learning Engineer preparing a multimodal training dataset. The dataset pairs video frames from a robot's camera feed with tabular telemetry logs (CSVs). 

Unfortunately, the telemetry logging system experienced intermittent sync errors and sensor glitches. You need to write a Rust filter program that sanitizes this data by rejecting corrupted telemetry files.

You are provided with:
1. A reference video file: `/app/sync_feed.mp4`.
2. A directory of expected good CSVs: `/app/corpora/clean/`.
3. A directory of known corrupted CSVs: `/app/corpora/evil/`.

Write a Rust CLI application located at `/home/user/telemetry_filter/` (you should initialize the cargo project). 
The application must accept a single argument (the path to a CSV file) and output exactly `VALID` or `INVALID` to standard output.

A telemetry CSV is considered `VALID` if and only if it meets BOTH of the following conditions:
1. **Sync Check:** The number of data rows in the CSV (excluding the header) exactly matches the total number of frames in the `/app/sync_feed.mp4` video. You will need to extract or count the frames of this video to determine the target number.
2. **Sensor Covariance Check:** The Pearson correlation coefficient ($r$) between the `sensor_alpha` and `sensor_beta` columns must be $\ge 0.85$. These sensors are physically coupled, so a correlation lower than this indicates a numerical accuracy error or sensor drift in the log.

If a CSV fails either check, it is `INVALID`. 

Your Rust application must be able to correctly classify 100% of the files in `/app/corpora/clean/` as `VALID` and 100% of the files in `/app/corpora/evil/` as `INVALID`.

**Execution format:**
Your program will be tested automatically using:
`cargo run --release -- <path_to_csv>`

Ensure your program prints only `VALID` or `INVALID` to stdout (along with any cargo build output, which goes to stderr). Do not print extra whitespace or debugging text to stdout.