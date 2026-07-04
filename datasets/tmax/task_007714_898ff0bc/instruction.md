You are an AI assistant helping a localization engineer. 

An automated ETL job that exports translation memories from our translation management system failed halfway through yesterday and had to be retried. Because of the retry, the log file `/home/user/translator_deliveries.txt` contains duplicate records for some translations.

Your task is to extract the latest translation updates from this log file and apply them to our master CSV database, `/home/user/master_en_es.csv`.

Here are the specific requirements:
1. **Extract**: Find all lines in `/home/user/translator_deliveries.txt` that represent an update. These lines look exactly like this:
   `[YYYY-MM-DD HH:MM:SS] UPDATE id="<string_id>" translation="<translated_text>"`
2. **Deduplicate**: If there are multiple updates for the same `string_id`, you MUST keep only the one with the most recent timestamp. Ignore older updates.
3. **Merge/Update**: Read `/home/user/master_en_es.csv`. This file has the header `string_id,en_text,es_text,status`.
   - For every `string_id` in the master CSV that has a valid update from step 2, replace the `es_text` field with the new `<translated_text>` and change the `status` field to `updated`.
   - If a `string_id` from the master file does not appear in the updates, leave its row unchanged.
   - If an update is for a `string_id` that does NOT exist in the master CSV, ignore it completely.
4. **Output**: Save the final merged data to `/home/user/updated_master.csv`. The output must maintain the original header, maintain the original row order as much as possible (or just sorted by `string_id`), use comma separation without extra quotes (assume no commas exist within the text fields themselves), and have exactly 4 columns per row.

You must only use standard Linux shell tools (Bash built-ins, awk, sed, grep, sort, join, etc.) to accomplish this task.