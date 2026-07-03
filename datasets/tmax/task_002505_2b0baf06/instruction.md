You are a data analyst building a high-performance stream processing pipeline in C to handle sensor data. We have an old configuration image at `/app/weights.png` that contains the specific weights and fallback threshold for our gap-filling algorithm.

First, use OCR (e.g., `tesseract`) to extract the parameters from `/app/weights.png`. The image contains text specifying three weights (`W1`, `W2`, `W3`) and a `THRESHOLD`.

Next, write a C program at `/home/user/processor.c` and compile it to `/home/user/processor`. This program must:
1. Read CSV lines from `stdin` continuously until EOF. The input format is: `Timestamp,SensorName,Value`
   - `Timestamp`: an integer.
   - `SensorName`: a UTF-8 string (up to 64 bytes).
   - `Value`: a float.
2. **Standardization (Unicode/Text):** Convert the `SensorName` to uppercase. To keep it simple and avoid external libraries, strictly convert only ASCII lowercase letters ('a'-'z') to uppercase ('A'-'Z'). Leave all other bytes (including UTF-8 multi-byte characters) exactly as they are.
3. **Resampling & Windowed Aggregation:** 
   - A `Value` of exactly `-1.0` indicates a missing reading (a gap).
   - Maintain a rolling history of the last 3 *valid* (non -1.0) values seen across the entire stream.
   - If a gap (-1.0) is encountered, replace it with the weighted sum of the last 3 valid values: `(W1 * oldest_valid) + (W2 * middle_valid) + (W3 * newest_valid)`.
   - If a gap is encountered but fewer than 3 valid values have been seen so far in the stream, replace the missing value with the `THRESHOLD` extracted from the image.
   - Valid values should be updated in your rolling history *before* processing the next line. Missing values (and their filled replacements) are *not* added to the rolling history.
4. Output the processed line to `stdout` in the format: `Timestamp,NormalizedSensorName,ProcessedValue`.
   - The `ProcessedValue` must be printed with exactly 2 decimal places (e.g., `%.2f`).

Ensure your program handles potentially millions of lines efficiently and accurately matches standard data stream processing behavior. Your compiled binary `/home/user/processor` will be aggressively tested against a reference implementation with random streams of data.