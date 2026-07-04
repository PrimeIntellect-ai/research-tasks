You are a data engineer tasked with cleaning up after an ETL pipeline failure. The pipeline was automatically retried, which resulted in near-duplicate log records being ingested across different file formats. Your goal is to consolidate these files, identify near-duplicates using text similarity, and output a clean dataset.

You have two input files:
1. `/home/user/data/batch1.csv` (Columns: `id`, `timestamp`, `log_message`)
2. `/home/user/data/batch2.json` (An array of JSON objects with keys: `id`, `timestamp`, `log_message`)

You need to write a script (in any language you choose) to perform the following steps:
1. Read both files and combine the records into a single dataset.
2. Tokenize and normalize the `log_message` for each record:
   - Convert the text to lowercase.
   - Remove all punctuation (keep only alphanumeric characters and spaces).
   - Split the text by whitespace to create a mathematical set of unique words/tokens.
3. Compare every record against every other record using **Jaccard Similarity** on their token sets. (Jaccard Similarity = Size of Intersection / Size of Union).
4. If two records have a Jaccard Similarity of **0.75 or higher**, they are considered duplicates. 
5. For any set of duplicate records, keep ONLY the record with the **smallest `timestamp`** (the original log). Discard the others. (Assume all timestamps are integers. If timestamps are tied, keep the one with the smaller `id`).
6. Write the final deduplicated records to `/home/user/output/clean_logs.jsonl`. Each line must be a valid JSON object with the keys `id`, `timestamp`, and `log_message`, sorted in ascending order by `id`.

Create the output directory `/home/user/output` if it does not exist. Ensure your code handles the multi-format ingestion and distance computation accurately.