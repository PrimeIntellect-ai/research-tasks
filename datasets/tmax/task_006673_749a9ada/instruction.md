You are an AI assistant helping a biomedical researcher organize and analyze cross-format datasets. 

The researcher has two datasets located in the home directory:
1. A relational SQLite database `/home/user/research.db`
2. A document-based JSON Lines file `/home/user/readings.jsonl`

The `research.db` contains two tables:
- `participants`: Contains participant demographic data.
- `trials`: Contains metadata about specific experimental trials.

The `readings.jsonl` file contains longitudinal sensor readings in JSON format. Each line is a JSON object with keys: `trial_id`, `timestamp`, and `sensor_data` (a nested object containing various metrics, including `heart_rate`).

**Your Task:**
Write a Python script at `/home/user/process_data.py` that performs the following:
1. Queries the SQLite database to identify all `participant_id`s who belong to the `cohort` named `'control'`, AND have trials with the `condition` named `'fasting'`.
2. Maps these relational records to the document-based `readings.jsonl` file using the corresponding trial IDs.
3. Calculates the average `heart_rate` for each of these specific participants during their 'fasting' trials. 
4. Outputs the final aggregated data into a JSON file at `/home/user/results.json`.

**Output Specification for `/home/user/results.json`:**
The file must contain a single JSON array of objects, sorted alphabetically by `participant_id`. Each object must have exactly two keys:
- `participant_id` (string)
- `avg_heart_rate` (float, rounded to exactly 2 decimal places)

Example output format:
```json
[
  {"participant_id": "P001", "avg_heart_rate": 72.50},
  {"participant_id": "P004", "avg_heart_rate": 68.33}
]
```

Run your script to ensure the `results.json` file is generated correctly.