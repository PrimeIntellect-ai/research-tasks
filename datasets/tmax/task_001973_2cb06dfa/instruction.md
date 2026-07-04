You are a data analyst acting as an algorithmic engineer. We need a lightweight, high-performance C pipeline to process raw IoT sensor data, handle missing values and outliers, enforce data schemas, and apply a pre-trained linear regression model for risk scoring.

Your task is to create a complete, reproducible bash-and-C pipeline.

**Step 1: The C Inference & Cleaning Engine**
Write a C program located at `/home/user/scorer.c` that does the following:
1.  **Read Model Weights:** First, read the file `/home/user/weights.txt` (which will be present before you start). It contains three lines in the exact format:
    `w_temp=<float>`
    `w_press=<float>`
    `bias=<float>`
2.  **Read and Clean Data:** Read `/home/user/sensor_data.csv` line by line. The CSV has a header: `timestamp,sensor_id,temperature,pressure`.
    *   **Schema Enforcement:** If `sensor_id` is not exactly `1`, `2`, or `3` (integer), drop the row. If `pressure` is empty or cannot be parsed as a float, drop the row.
    *   **Missing Value & Outlier Handling:** If `temperature` is empty, "NaN", or outside the valid range of `[-50.0, 150.0]`, impute it to a default value of `20.0`.
3.  **Inference:** For each valid row, compute the risk score using the formula:
    `risk_score = (temperature * w_temp) + (pressure * w_press) + bias`
4.  **Output:** Write the processed and scored rows to `/home/user/scored_data.csv`. The output must include a header `timestamp,sensor_id,risk_score`. The `risk_score` must be formatted to exactly two decimal places (e.g., `%.2f`).

**Step 2: The Reproducible Pipeline**
Create a Bash script at `/home/user/pipeline.sh` that acts as the reproducible pipeline. When executed, it must:
1.  Compile `/home/user/scorer.c` into an executable named `/home/user/scorer` (using `gcc`).
2.  Execute `/home/user/scorer`.
3.  Use `awk` (or standard bash tools) to read `/home/user/scored_data.csv` and calculate the average `risk_score` for each valid `sensor_id`.
4.  Write these averages to `/home/user/summary.txt` in the format `sensor_id: average_score` (one per line, sorted numerically by `sensor_id`, average score formatted to 2 decimal places).

**Constraints:**
*   You must write the code strictly in C (for the engine) and Bash (for the pipeline wrapper). Standard libraries (`stdio.h`, `stdlib.h`, `string.h`) are sufficient.
*   Ensure your Bash script has executable permissions.