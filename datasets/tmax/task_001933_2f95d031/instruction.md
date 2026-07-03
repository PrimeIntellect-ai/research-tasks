You are an automation specialist tasked with building a robust data processing workflow for an e-commerce platform. 

We have a raw event log file located at `/home/user/raw_events.jsonl`. This file contains JSON lines representing user interactions. 
Your goal is to write and execute a Python script that reads this file, cleans and deduplicates the data, performs stratified sampling to create a balanced dataset, and writes a strict execution log.

Here are the exact requirements for your pipeline:

1. **Cleaning and Normalization:**
   - Read the records from `/home/user/raw_events.jsonl`.
   - Each record should have `user_id`, `item_id`, `action`, and `timestamp`.
   - **Drop missing fields**: If any of these 4 keys are missing, drop the record.
   - **Normalization**: Normalize the `action` field into three distinct lowercase categories:
     - If the original action string contains "view" (case-insensitive), normalize it to `"view"`.
     - If it contains "click" (case-insensitive), normalize it to `"click"`.
     - If it contains "purchase" or "buy" (case-insensitive), normalize it to `"purchase"`.
     - If it matches none of these, drop the record (classify as "unknown action").
   - **Deduplication**: Remove exact duplicate records. A record is a duplicate if it has the exact same `user_id`, `item_id`, normalized `action`, and `timestamp` as a previously seen record. Keep only the first occurrence.

2. **Stratified Sampling:**
   - From the cleaned, normalized, and deduplicated records, take a stratified sample of **exactly 100 records per action category** (`view`, `click`, `purchase`). 
   - If a category has fewer than 100 records, include all of its valid records.
   - **Deterministic Sampling**: To ensure reproducibility, for each category, sort the valid records primarily by `timestamp` (ascending) and secondarily by `user_id` (ascending). Then select the first N records.
   - Write the final sampled dataset to `/home/user/sampled_events.jsonl`. Keep the JSON lines format, but ensure the `action` field contains the *normalized* value.

3. **Pipeline Logging:**
   - Create a JSON log file at `/home/user/pipeline_run.json`.
   - The log file must contain exactly this structure:
     ```json
     {
       "records_read": <total lines in raw_events.jsonl>,
       "dropped_missing_fields": <count of dropped records due to missing fields>,
       "dropped_unknown_action": <count of records dropped due to unmappable actions>,
       "duplicates_removed": <count of duplicate records removed>,
       "final_counts": {
         "view": <number of views in the final sampled output>,
         "click": <number of clicks in the final sampled output>,
         "purchase": <number of purchases in the final sampled output>
       }
     }
     ```

Please write and run the Python script to complete these steps. Ensure that the paths and file formats exactly match the specifications.