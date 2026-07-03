You are a localization engineer managing a continuous translation pipeline. A previous pipeline step, written poorly in bash, silently corrupted or dropped rows from your translation exports because the translation text fields contained embedded newlines.

You have a large CSV file located at `/home/user/translations.csv` containing raw translation logs. 

The CSV has the following strict format:
`timestamp,locale,msg_id,"translated_text"`

- `timestamp`: A standard UNIX epoch integer.
- `locale`: A 5-character string like `es_ES` or `fr_FR`.
- `msg_id`: An alphanumeric string without spaces or special characters.
- `"translated_text"`: The translation text. This field is *always* enclosed in double quotes. It frequently contains embedded newline characters (`\n`).

Your task is to write a C program that streams this file (without loading the entire file into memory at once) and calculates a specific text-density feature for the Spanish locale (`es_ES`), aggregated by the hour.

Write your C code in `/home/user/process_loc.c`, compile it to `/home/user/process_loc`, and run it to produce an output file at `/home/user/hourly_stats.csv`.

**Program Requirements:**
1. **Streaming & Parsing**: Read `/home/user/translations.csv` sequentially. You must correctly parse records where `"translated_text"` spans multiple lines due to embedded newlines. Do not use an external CSV library; write a simple character-by-character or state-based stream processor.
2. **Filtering**: Process only records where `locale` is exactly `es_ES`.
3. **Timestamp Bucketing**: Group the valid records into 1-hour buckets. The bucket timestamp is the beginning of the hour (e.g., timestamp divided by 3600, then multiplied by 3600).
4. **Feature Extraction**: For each valid record, count the number of standard ASCII alphabetical characters (`A-Z` and `a-z`) inside the `translated_text` field. Ignore spaces, punctuation, numbers, and newlines.
5. **Aggregation & Output**: Sum the extracted character counts for each hour bucket. Write the results to `/home/user/hourly_stats.csv` in the format `bucket_epoch,total_alpha_chars`, sorted chronologically.

**Example input snippet:**
```csv
1700000000,es_ES,btn_ok,"Aceptar"
1700001000,es_ES,msg_welcome,"Hola,
bienvenido"
1700001500,fr_FR,msg_welcome,"Bonjour
!"
1700004000,es_ES,msg_err,"Error
grave
."
```

**Corresponding output snippet (`/home/user/hourly_stats.csv`):**
```csv
1699999200,21
1700002800,10
```
*(Explanation: 1700000000 and 1700001000 belong to bucket 1699999200. 'Aceptar' has 7 letters, 'Hola,\nbienvenido' has 14 letters. Total = 21. 1700004000 is in bucket 1700002800. 'Error\ngrave\n.' has 10 letters.)*