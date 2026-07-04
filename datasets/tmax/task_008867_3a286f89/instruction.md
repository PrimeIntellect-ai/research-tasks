You are a Data Engineer building an ETL pipeline to analyze customer service logs from a recent A/B test. We need to process the raw text data, tokenize it, track our experiment metrics, and run a hypothesis test to see if our new response protocol (Group B) significantly reduced resolution times compared to the control (Group A).

Your task is to build a two-part pipeline using Bash and Python. 

**Step 1: Dataset Preparation (Bash/jq/awk)**
There is a raw data file located at `/home/user/data/raw_logs.jsonl`. Each line is a JSON object with keys: `id`, `text`, `experiment_group` ("A" or "B"), and `resolution_time` (float).
Write a Bash script that processes this file to create a clean CSV at `/home/user/data/clean_logs.csv` with the headers: `id,experiment_group,resolution_time,token_count`.
To calculate `token_count`:
1. Convert the `text` field to lowercase.
2. Remove all punctuation (anything that is not a word character `[a-zA-Z0-9_]` or whitespace).
3. Split the text by whitespace to count the tokens.
4. **Filter:** Only include rows in your output CSV where `token_count` is strictly greater than 10.

**Step 2: Experiment Tracking & Hypothesis Testing (Python)**
Write a Python script that reads `/home/user/data/clean_logs.csv` and performs a statistical analysis on the filtered data.
1. Calculate the mean `resolution_time` for Group A and Group B.
2. Perform a standard independent two-sample t-test (assume **equal variances**) to compare the resolution times of Group A and Group B.
3. Calculate the 95% Confidence Interval for the difference in means (`Mean A - Mean B`). Use the standard Student's t-distribution critical value for this equal-variance CI.
4. Save the experiment metrics into a JSON file at `/home/user/etl_output/results.json`.

The `/home/user/etl_output/results.json` file must have exactly this format (round all floats to 4 decimal places):
```json
{
  "valid_records": 120,
  "group_a_mean": 45.1234,
  "group_b_mean": 38.5678,
  "ci_lower": 1.2345,
  "ci_upper": 12.3456,
  "p_value": 0.0345
}
```

Ensure the directories exist. You may use `pip install scipy pandas` if needed. Keep all your scripts in `/home/user/`.