You are an MLOps engineer tasked with building a deterministic verification tool for experiment metric tracking. 

As part of our CI/CD pipeline, we compare incoming experiment metrics against a historical baseline. The historical baseline is stored in a 16-bit Mono WAV audio file located at `/app/experiment_baseline.wav`. The PCM sample values in this audio file actually represent our historical metric distribution.

Your task is to write a script that processes a batch of new experiment metrics and compares them to the baseline.

First, extract the baseline distribution from the audio file:
1. Read `/app/experiment_baseline.wav`.
2. Extract the integer PCM values (16-bit).
3. Filter out any values less than or equal to 0.
4. Keep exactly the first 1000 positive integers. This is your `baseline_distribution`.

Second, write an executable script at `/home/user/metric_analyzer.py` (you may use Python) that reads CSV data from `stdin` and outputs a specific JSON structure to `stdout`.

The script must do the following on each execution:
1. Read `stdin` until EOF. The input will be a CSV-formatted string with a header: `experiment_name,metric_value`.
2. Filter the incoming data: Ignore any rows where `metric_value` cannot be parsed as a float, or where `metric_value <= 0`.
3. If there are fewer than 2 valid rows after filtering, output exactly: `{"p_value": -1.0000, "vowel_embedding": [0, 0, 0, 0, 0]}` and exit.
4. If there are 2 or more valid rows:
   - Run a two-sided Welch's t-test (assuming unequal variances) between the valid incoming `metric_value`s and the `baseline_distribution` (from the WAV file). Compute the p-value.
   - Compute a simple feature "embedding" of the valid experiment names: Count the total occurrences of each lowercase vowel `['a', 'e', 'i', 'o', 'u']` across all valid `experiment_name` strings (case-insensitive).
5. Output a JSON object with two keys:
   - `"p_value"`: The calculated p-value formatted as a float rounded to exactly 4 decimal places (e.g., `0.0412`).
   - `"vowel_embedding"`: A list of 5 integers representing the counts of `[a, e, i, o, u]`.

Example Output:
`{"p_value": 0.8123, "vowel_embedding": [12, 4, 0, 7, 1]}`

Requirements:
- Your script must be strictly deterministic and bit-exact in its output.
- Print ONLY the JSON to `stdout`. Do not print any debugging information to `stdout`.
- Be sure to include the shebang `#!/usr/bin/env python3` and make the script executable (`chmod +x /home/user/metric_analyzer.py`).