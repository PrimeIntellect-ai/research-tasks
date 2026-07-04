You are an algorithmic data scientist working in a restricted environment. You need to analyze a corrupted telemetry video feed, clean the extracted data strictly enforcing a data schema, calculate statistical bounds, and serve the results over a network protocol.

**1. Data Extraction (Video Analysis)**
You are provided with a video artifact at `/app/telemetry.mp4`. Each frame of this video represents a time step in a telemetry feed, and the mean grayscale pixel intensity of the frame represents the sensor reading for that time step.
- Extract the frames from the video.
- For each frame (ordered by frame number, starting at 1), calculate the mean grayscale intensity (a value between 0.0 and 1.0).
- Multiply this intensity by 1000 and round to the nearest whole number to get the raw integer sensor reading.

**2. Data Cleaning & Schema Enforcement**
The sensor occasionally drops out, resulting in frames that are almost entirely black (raw integer value < 10).
- Create a strict Bash pipeline to clean this data. If a raw value is less than 10, it must be considered a missing value (NaN).
- **Crucial Schema Rule:** The downstream analysis requires strictly integer values. You must impute any missing values by using the linear interpolation (average) of the nearest valid preceding and succeeding frames, rounded to the nearest integer. If the first or last frame is missing, fall back to the nearest valid frame.
- Save this cleaned dataset to `/home/user/cleaned_telemetry.csv` in the format `frame_number,sensor_value`.

**3. Statistical Modeling (Bootstrap)**
Write a Bash/awk script to perform a bootstrap analysis on the cleaned sensor values to estimate the mean and the 95% confidence interval.
- Perform exactly 10,000 bootstrap resamples (with replacement) of the cleaned values.
- **Important:** To ensure reproducibility, your `awk` script must initialize its random number generator with a specific seed before the bootstrap loop: `srand(42)`. (Note: awk's rand() behaves differently across implementations; use standard GNU awk `gawk`).
- Calculate the mean of each resample.
- Determine the overall mean, the 2.5th percentile (lower bound), and the 97.5th percentile (upper bound) of these 10,000 means. Round all final statistics to two decimal places.

**4. Service Integration (TCP Verifier)**
You must create a TCP server listening on `127.0.0.1:9090`. You may use `socat` or `nc` combined with a bash loop or coproc. The server must handle incoming text requests and respond accordingly, keeping the connection open or closing it after the response (verifier will send one command per connection):
- Request `SCHEMA\n`: The server must respond with exactly `frame_number:int,sensor_value:int\n`.
- Request `DATA <frame_number>\n` (e.g., `DATA 5`): The server must respond with the cleaned integer value for that specific frame, followed by a newline.
- Request `STATS\n`: The server must respond with exactly `mean:<mean>,lower:<lower>,upper:<upper>\n` using the bootstrap results.

Ensure your TCP server is running in the background and is ready to accept connections before finishing your workflow.