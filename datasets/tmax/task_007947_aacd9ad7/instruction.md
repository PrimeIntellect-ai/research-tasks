You are helping a data scientist debug and automate a data cleaning pipeline. They have a high-performance C program designed to join sensor readings with calibration data and apply a mathematical transformation. However, the C program currently outputs all zeros or garbage values for the numerical columns (similar to rendering a blank plot due to a silent configuration error). 

Your objective is to fix the schema enforcement issue in the C program, and then build a reproducible bash pipeline to process the data.

Here is the setup:
- The sensor data is at `/home/user/data/sensors.csv` (Format: `id,timestamp,value`).
- The calibration data is at `/home/user/data/calibration.csv` (Format: `id,offset,multiplier`).
- The buggy C source code is at `/home/user/src/clean_join.c`.

The C program is supposed to:
1. Load the calibration data into memory.
2. Stream the sensor data.
3. For each sensor reading, find the corresponding calibration `offset` and `multiplier` by `id`.
4. Calculate the cleaned value: `cleaned_value = (value + offset) * multiplier`
5. Print the result to standard output in the format: `id,timestamp,cleaned_value` (where `cleaned_value` is printed with exactly 2 decimal places, e.g., `%.2f`).

Tasks:
1. **Fix the C Code**: Identify and fix the bug in `/home/user/src/clean_join.c`. The bug is related to strict data schema and type parsing (hint: check how doubles are parsed).
2. **Build the Pipeline**: Create a bash script at `/home/user/pipeline.sh` that:
   - Compiles the fixed C program into an executable named `clean_join` in `/home/user/src/`.
   - Runs the executable, passing the sensor and calibration files as arguments (in that order: `./clean_join <sensors.csv> <calibration.csv>`).
   - Captures the output.
   - Sorts the output numerically by the `id` column (the first column).
   - Saves the final sorted output to `/home/user/output/final_data.csv`.

Ensure your pipeline is completely reproducible and runs without user intervention. Make sure `/home/user/pipeline.sh` has executable permissions.