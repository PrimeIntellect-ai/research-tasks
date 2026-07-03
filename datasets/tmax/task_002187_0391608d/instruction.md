You are a data engineer tasked with recovering corrupted telemetry data from a backup system. The raw text logs were lost, but a screen recording of the log monitor was saved as a video file located at `/app/telemetry_backup.mp4`. 

Your objective is to build a multi-stage ETL pipeline in Go and Bash to extract, transform, and load this mathematical data.

**Pipeline Requirements:**

1. **Extraction (Bash/CLI):**
   - Extract frames from `/app/telemetry_backup.mp4` at a rate of 2 frames per second. `ffmpeg` and `tesseract-ocr` are pre-installed on the system.
   - Run Tesseract OCR on the extracted frames to recover the text logs.

2. **Parsing & Streaming (Go):**
   - Write a Go program at `/home/user/pipeline.go` that streams the potentially massive raw text output from the extraction phase.
   - Use Regex pattern matching in Go to find valid telemetry lines. The valid format in the logs looks like this (allowing for variable whitespace):
     `[TELEMETRY] NODE:<4-character-alphanumeric> P:<float> V:<float> A:<float>`
     *(Example: `[TELEMETRY] NODE:X7B2 P:12.5 V:4.02 A:0.98`)*
   - Silently ignore any lines that do not strictly match this pattern or contain OCR artifacts/garbage.

3. **Mathematical Transformation:**
   - For every valid parsed line, calculate the mathematical pseudo-energy metric $E$ using the formula: 
     $E = P \times (V^2) + \sqrt{A}$
   - Keep a running sum of $E$ for each unique `NODE`.

4. **Loading (Output):**
   - Your Go program must output the final aggregated data as a JSON file at `/home/user/energy_totals.json`.
   - The JSON format must be a single dictionary mapping the 4-character NODE IDs to their total summed $E$ (as floats).
     Example: `{"X7B2": 1542.33, "A1N9": 88.01}`

Build, test, and run your pipeline. Because OCR is imperfect, your final values do not need to be 100% exact to the decimal, but they must be statistically very close to the true underlying values in the video.