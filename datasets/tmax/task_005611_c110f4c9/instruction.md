You are an MLOps engineer tasked with processing experiment logs. We need to parse a CSV file containing experiment results, strictly enforce a data schema, and track the valid experiments in a structured JSON Lines format.

Your task is to write a C++ program `/home/user/process_experiments.cpp` that does the following:

1. **Dependency Installation**: Your program must use the `nlohmann/json` library for JSON serialization. You should download the single-header version of this library using:
   `wget https://raw.githubusercontent.com/nlohmann/json/v3.11.2/single_include/nlohmann/json.hpp -O /home/user/json.hpp`

2. **Schema Enforcement**: Read the input CSV file located at `/home/user/experiments.csv`. The CSV has a header row: `experiment_id,accuracy,epoch_count,status`.
   Validate each data row (excluding the header) against the following strict schema:
   - `experiment_id`: Must be a string starting exactly with the prefix `EXP_`
   - `accuracy`: Must be a valid floating-point number between `0.0` and `1.0` (inclusive).
   - `epoch_count`: Must be a valid integer strictly greater than `0`.
   - `status`: Must be a string, exactly either `SUCCESS` or `FAILED`.

3. **Experiment Tracking**: 
   - For every **valid** row, create a JSON object with the keys `"experiment_id"`, `"accuracy"`, `"epoch_count"`, and `"status"`. Append this JSON object as a single line to `/home/user/tracked_artifacts.jsonl` (JSON Lines format).
   - For every **invalid** row, append the 0-indexed row number (where the first data row after the header is index 0) to a text file `/home/user/invalid_rows.log`, one number per line.

Requirements:
- Compile your program using `g++ -std=c++11 /home/user/process_experiments.cpp -o /home/user/process_experiments`.
- Execute your compiled program.
- Ensure that the output files `/home/user/tracked_artifacts.jsonl` and `/home/user/invalid_rows.log` are correctly formatted.

Make sure to handle potential type conversions carefully (e.g. string to float/int) and catch exceptions if a field is completely malformed (e.g., text instead of a number), marking those rows as invalid.