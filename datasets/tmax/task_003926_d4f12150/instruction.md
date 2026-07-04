You are an AI assistant acting as a data scientist. We are processing a time-series dataset of multilingual social media posts to filter out coordinated bot networks. 

You need to build a Rust-based detector to classify JSONL log files as either "clean" or "anomalous" (bot-generated). 

Here is the specification for the detector:
1. **Input:** The program should take a single file path as a command-line argument. The file is a JSONL file where each line is a JSON object with a `timestamp` (integer) and `text` (string) field. The lines are ordered by timestamp.
2. **Algorithm:** 
   - Maintain a rolling window of the most recent `W` messages.
   - For every new message read, if the window is fully populated (contains exactly `W` messages), compute the Levenshtein distance between the new message's `text` and the `text` of each of the `W` messages in the window.
   - Calculate the arithmetic mean of these `W` distances (this is the rolling average distance).
   - A message is flagged as an ANOMALY if **both** of the following conditions are met:
     a) The rolling average Levenshtein distance is strictly less than `D`.
     b) The message's `text` contains at least one character belonging to the specific target Unicode script `S`.
   - As soon as an anomaly is detected, the program must immediately terminate with **exit code 1**.
   - If the entire file is processed without detecting any anomalies, the program must terminate with **exit code 0**.
   - After processing a message (whether the window was full or not), add the new message to the rolling window (discarding the oldest if the window exceeds size `W`).
3. **Parameters:**
   The exact values for `W` (window size), `D` (distance threshold), and `S` (target Unicode script) were written on a whiteboard. A photo of this whiteboard is located at `/app/config.png`. You will need to extract these parameters from the image first (tools like `tesseract` are available).

Create the Rust project in `/home/user/bot_detector`. Provide instructions on how to compile it. Your final solution must be a compiled binary located at `/home/user/bot_detector/target/release/bot_detector` that takes the file path as its first and only argument.

Note: You can use the `strsim` crate for Levenshtein distance and `unicode-blocks` or standard character ranges for script detection.