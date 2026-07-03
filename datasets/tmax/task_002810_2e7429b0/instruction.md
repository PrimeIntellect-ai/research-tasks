You are an automation specialist building a data ingestion workflow for an international IoT sensor network. The incoming data contains multi-lingual diagnostic text and a sequence of numeric sensor readings, but the data is often noisy: strings contain typos, and the sensor readings have dropped packets (represented as missing values).

Your task is to write a Go program that processes a JSONL (JSON Lines) file, cleans the data, and computes necessary metrics. 

**Input Data:**
A file exists at `/home/user/raw_data.jsonl`. Each line is a JSON object with the following schema:
- `id` (integer)
- `text_a` (string): The expected diagnostic message.
- `text_b` (string): The actual received diagnostic message, which may contain typos. Contains various Unicode characters (Emojis, Cyrillic, CJK, etc.).
- `series` (array of float64 or null): A sequence of sensor readings. Missing readings are represented as `null`.

**Processing Requirements:**
Create a Go program at `/home/user/process.go` that reads `/home/user/raw_data.jsonl` and performs the following operations for each line:

1. **Interpolation (Imputation):**
   The `series` array contains `null` values where data was dropped. You must replace these `null` values using **linear interpolation** based on the nearest non-null surrounding values. 
   - You can assume the first and last values in the `series` array are never `null`.
   - If there are multiple consecutive `null` values, you must interpolate them evenly. For example, `[5.0, null, null, 20.0]` should become `[5.0, 10.0, 15.0, 20.0]`.

2. **Distance Computation:**
   Calculate the Levenshtein distance between `text_a` and `text_b`. 
   - **CRITICAL:** The distance must be calculated based on **Unicode runes**, not bytes. For example, the distance between `"🌍"` and `"🌎"` is 1, not the difference in their byte lengths. 
   - You must implement this distance calculation yourself in standard Go (do not use external third-party libraries for the Levenshtein algorithm).

**Output Data:**
Your Go program should output the processed records to a new file at `/home/user/processed_data.jsonl`.
Each line must be a JSON object containing:
- `id` (integer)
- `text_a` (string): unchanged
- `text_b` (string): unchanged
- `series` (array of float64): The fully interpolated series (no nulls).
- `text_distance` (integer): The calculated rune-based Levenshtein distance.

Run your Go program to generate the final `/home/user/processed_data.jsonl` file. Do not leave `null` values in the output JSON.