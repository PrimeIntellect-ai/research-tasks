You are a localization engineer managing a translation pipeline. An ETL job that processes translation batches often retries on failure, resulting in duplicate records across different batch files. You need to write a C++ program to merge the batches, normalize the data, deduplicate, and compute rolling statistics on translation quality scores.

You are provided with two CSV files in `/home/user/inputs/`:
- `batch1.csv`
- `batch2.csv`

Both files have the following columns:
`msg_id,lang,translation,timestamp,score`

Your task is to write and execute a C++ program (compile it with `g++ -std=c++17` or later) that performs the following steps:

1. **Union and Merge**: Read all records from both `batch1.csv` and `batch2.csv`.
2. **Normalization**: Normalize the `lang` column. The input might have formats like `En_us`, `fr_FR`, `es_es`. You must standardize it to the format `ll-CC` where `ll` is exactly two lowercase letters, followed by a hyphen `-`, followed by exactly two uppercase letters (e.g., `en-US`, `fr-FR`, `es-ES`).
3. **Deduplication**: The ETL retry process creates duplicates. For any given `msg_id` and normalized `lang`, keep ONLY the record with the highest `timestamp`. (Assume all highest timestamps for a given `msg_id` and `lang` combination are unique).
4. **Rolling Statistics**: For each normalized `lang`, sort the deduplicated records by `timestamp` in ascending order. Then, calculate a moving average of the `score` over a rolling window of the last 3 records (including the current one). 
   - For the 1st record, the average is just its own score.
   - For the 2nd record, it's the average of the 1st and 2nd.
   - For the 3rd, it's the average of the 1st, 2nd, and 3rd.
   - For the 4th, it's the average of the 2nd, 3rd, and 4th, and so on.
5. **Output**: Write the final processed data to `/home/user/output/final_translations.csv`. 
   - The output CSV must have the following header: `msg_id,lang,timestamp,score,rolling_avg_score`
   - The rows must be sorted by the normalized `lang` alphabetically (ascending), and then by `timestamp` ascending.
   - The `rolling_avg_score` must be formatted to exactly 2 decimal places (e.g., `88.50`, `90.00`).

Ensure your output directory exists before writing to it. You are only allowed to use standard C++ libraries (no external libraries like Boost or Pandas-equivalent).