You are an MLOps engineer analyzing corrupted experiment logs. To bypass legacy storage limits, continuous sensor readings were encoded directly into a video file stream, but the stream contains periodic transmission dropouts.

Your objective is to extract the data, detect anomalies, and write a robust, Bash-only stream processing script to reconstruct the data and calculate a local second-derivative filter. 

**Step 1: Video Extraction & Storage**
The sensor video is located at `/app/sensor_feed.mp4`. 
Create a directory `/home/user/frames/`. Use `ffmpeg` to extract the frames from this video at exactly 1 frame per second (1 fps) as JPEG images, naming them sequentially as `%04d.jpg` (e.g., `0001.jpg`, `0002.jpg`, etc.).

**Step 2: Outlier Detection**
We will use the file sizes of these frames as a proxy for the sensor data. 
Generate a text file at `/home/user/raw_sizes.txt` containing the file sizes (in bytes) of the extracted frames, in numerical order (one per line). 
*Constraint:* If a frame's file size is strictly less than `5000` bytes, it is a transmission dropout. Write the string `NaN` instead of the file size for that frame.

**Step 3: Missing Value Imputation and Linear Filtering Script**
Due to a previous pipeline bug where pandas silently converted integer sensor readings to floats (causing downstream schema errors), you must write a strict, pure Bash/CLI script (using Bash built-ins, `awk`, `sed`, `bc`, etc.) to process the data stream safely.

Create an executable script at `/home/user/process_stream.sh`.
This script must read a sequence of lines from standard input (`stdin`). Each line will contain either a positive integer or the string `NaN`. For each input line, the script must print a single line to standard output (`stdout`) containing exactly two comma-separated integers: `ImputedValue,FilterValue`.

*   **ImputedValue Rules:**
    *   If the input is an integer, `ImputedValue` is that integer.
    *   If the input is `NaN`, `ImputedValue` is the integer *floor* of the arithmetic mean of the up to 3 most recently outputted `ImputedValue`s. 
    *   If the input is `NaN` and no previous values exist, `ImputedValue` is `0`.
*   **FilterValue (Linear Algebra) Rules:**
    *   Compute the dot product of the fixed vector `[1, -2, 1]` with the 3 most recently outputted `ImputedValue`s (specifically: `(1 * V_current) + (-2 * V_prev1) + (1 * V_prev2)`).
    *   If fewer than 3 values have been processed so far, `FilterValue` is `0`.

Run your script against `/home/user/raw_sizes.txt` and save the final output to `/home/user/processed_metrics.csv`.

*Note:* Your script `/home/user/process_stream.sh` must be robust to streams of arbitrary length and must exactly follow the mathematical rules above. It will be rigorously fuzzed against a reference implementation.