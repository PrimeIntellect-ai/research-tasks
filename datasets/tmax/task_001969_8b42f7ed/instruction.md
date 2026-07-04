You are a localization engineer managing a translation pipeline. We recently switched to a new Machine Translation (MT) pre-translation system, and human translators are reviewing and editing the MT output. We need to identify translators who are struggling with the new system or receiving consistently poor MT suggestions, indicated by a sudden spike in their edit distances over time.

You are given two files in the `/home/user/localization_data/` directory:
1. `strings.csv`: Contains the translated strings.
   Columns: `string_id`, `language_code`, `original_text`, `translated_text`.
   Note: The `translated_text` contains multi-language Unicode strings (e.g., Arabic, CJK, Cyrillic).

2. `telemetry.csv`: Contains event logs of translators editing the strings.
   Columns: `timestamp`, `string_id`, `translator_id`, `edit_distance`.
   Note: The telemetry pipeline sometimes drops the `edit_distance` metric, resulting in empty values (nulls) for some rows.

Write a Python script to process this data. You may install standard data processing libraries like `pandas` if needed. Ensure your script performs the following operations:

1. **Merge**: Join the telemetry data with the strings data on `string_id`.
2. **Imputation**: For each `translator_id`, sort their edits by `timestamp` in ascending order. Fill any missing `edit_distance` values using Forward Fill (ffill). If the first record for a translator is missing, use Backward Fill (bfill) for that record after the forward fill.
3. **Unicode Normalization**: Calculate a `normalized_edit_distance` for each row, defined as the imputed `edit_distance` divided by the character length of the `translated_text` (use Python's standard `len()` function on the unicode string).
4. **Rolling Statistics**: For each `translator_id`, calculate a 3-record rolling average of the `normalized_edit_distance` (ordered by timestamp). Use `min_periods=1` so early records still get an average.
5. **Anomaly Detection**: An anomaly is detected if a record's rolling average strictly exceeds `0.50` (> 0.50). 

Output the anomalous records to a JSON file at `/home/user/localization_data/anomalies.json`. The JSON file should contain a list of objects, each representing an anomalous event, with the following keys exactly:
- `string_id` (string)
- `translator_id` (string)
- `language_code` (string)
- `timestamp` (string)
- `rolling_avg` (float, rounded to 3 decimal places)

Example format for `anomalies.json`:
```json
[
  {
    "string_id": "s4",
    "translator_id": "t1",
    "language_code": "ja",
    "timestamp": "2023-10-01T10:15:00Z",
    "rolling_avg": 0.556
  }
]
```
Ensure the JSON output is formatted as a valid list of objects.