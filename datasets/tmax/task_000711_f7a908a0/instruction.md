You are a localization engineer tasked with analyzing telemetry data to prioritize translation updates. 

You have two files in your environment:
1. `/home/user/telemetry.jsonl`: A very large streaming log file containing missing translation events from production. Each line is a JSON object with the following schema:
   `{"timestamp": "YYYY-MM-DDTHH:MM:SSZ", "lang": "locale_code", "string_id": "string_identifier"}`
2. `/home/user/string_metadata.csv`: A CSV file containing metadata for all string identifiers, with the header `string_id,module,priority`. Priorities can be `low`, `medium`, or `high`.

Your task is to process these files to find out which high-priority strings are missing most often, bucketed by hour and language. 

Specifically, you need to:
1. Extract the hour from the `timestamp` (format: `YYYY-MM-DDTHH`).
2. Join the telemetry data with the `string_metadata.csv` file using `string_id`.
3. Filter the records to include ONLY strings where the `priority` is `high`.
4. Aggregate the data to count the number of missing events (`missing_count`) per `hour`, `lang`, `string_id`, and `module`.
5. Write the final aggregated results to `/home/user/high_priority_missing.csv`.

The output file `/home/user/high_priority_missing.csv` must:
- Be a valid CSV file.
- Include the exact header: `hour,lang,string_id,module,missing_count`
- Be sorted by `hour` (ascending), then by `missing_count` (descending), and finally by `string_id` (ascending).

Process the file efficiently, as telemetry logs can be too large to load entirely into memory at once. You may use any language or standard Linux tools you prefer.