You are an AI assistant helping a data researcher organize and process a messy dataset. 

The researcher has an SQLite database located at `/home/user/research_data.db`. This database contains three tables: `sites`, `subjects`, and `trials`. 

Unfortunately, the database was created without explicit foreign key constraints. However, relationships implicitly exist based on a standard naming convention: a column named `<table>_id` always references the `id` column of the `<table>` table (e.g., `subject_id` references `id` in `subjects`).

Your task is to reverse engineer this data model, join the relevant data, and export it into a properly formatted, deeply nested JSON file.

Specifically, you need to:
1. Analyze the schema to confirm the implicit relationships between `trials`, `subjects`, and `sites`.
2. Write a script (in the language of your choice) to query the database and join these tables. You must extract all records from `trials`, along with their associated `subject` and the subject's associated `site`.
3. Export the joined results into a JSON file located at `/home/user/denormalized_trials.json`. 
4. The output JSON must be a JSON array of objects, where each object represents a trial and follows the exact nested structure required by the JSON schema located at `/home/user/trial_schema.json`.

The expected structure for each trial in the output JSON array is:
```json
[
  {
    "trial_id": <integer>,
    "date": "<string>",
    "outcome": "<string>",
    "score": <float>,
    "subject": {
      "subject_id": <integer>,
      "age": <integer>,
      "cohort_group": "<string>",
      "site": {
        "site_id": <integer>,
        "name": "<string>",
        "location": "<string>"
      }
    }
  }
]
```
Note: Ensure column names from the database are correctly mapped to the JSON keys (e.g., `id` in `trials` maps to `trial_id`, the `group_name` column in subjects maps to `cohort_group`, etc. Check the database schema and `trial_schema.json` to confirm exact mappings).

Please execute the necessary commands and code to generate `/home/user/denormalized_trials.json`.