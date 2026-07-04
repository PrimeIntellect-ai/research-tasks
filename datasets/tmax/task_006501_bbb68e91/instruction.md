You are an AI assistant helping a DevOps team process configuration drift logs. 

We have a configuration manager that exports daily changes into a CSV file located at `/home/user/config_drifts.csv`. 
The CSV has four columns: `id`, `timestamp`, `service`, and `diff`.

Recently, a poorly written bash pipeline was silently dropping rows where the `diff` column contained embedded newlines. We need a robust Python solution to process this file, ensuring no data is lost and that we extract the exact configuration additions.

Write a Python script at `/home/user/process_drifts.py` that performs the following steps:
1. **Read the CSV safely**: Properly parse `/home/user/config_drifts.csv`, correctly handling embedded newlines within the `diff` column (it is valid RFC 4180 CSV).
2. **Parallel Extraction**: Use Python's `multiprocessing` or `concurrent.futures` module to process the rows in parallel. For each row's `diff` text, extract all "added" configuration lines. An added line is defined as any line starting with exactly `"+ "` (a plus sign followed by a space). Strip the `"+ "` prefix from the extracted lines.
3. **Grouping and Sorting**: Group the extracted additions by the `service` name. Within each service's group, order the additions chronologically based on the `timestamp` (ascending order: oldest to newest). If a single `diff` contains multiple additions, preserve their top-to-bottom order from the diff.
4. **Output**: Save the results as a standard JSON file at `/home/user/drift_summary.json`. 

The JSON should have the following structure:
```json
{
  "service_name": [
    "first_added_config_chronologically",
    "second_added_config_chronologically"
  ],
  "another_service": [
    ...
  ]
}
```

Ensure your script runs efficiently, handles the embedded newlines correctly, and writes the final JSON output. Run your script to generate the `/home/user/drift_summary.json` file.