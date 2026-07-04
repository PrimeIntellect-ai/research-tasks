You are a localization engineer managing a translation pipeline. An unreliable upstream ETL job periodically appends raw localization strings to a log file at `/home/user/raw_translations.txt`. Because this ETL job frequently fails and retries, it produces duplicate translation records.

The format of `/home/user/raw_translations.txt` is:
`YYYY-MM-DDTHH:MM:SSZ|locale|translated_text`

Your task is to fix this data issue by writing a Rust program that buckets the records by hour, removes duplicates within the same hour and locale, and writes out a clean summary.

1. Write a Rust program at `/home/user/dedup.rs`.
2. The program must read from `/home/user/raw_translations.txt`.
3. It should bucket the timestamps to the hour level (i.e., truncate the timestamp to `YYYY-MM-DDTHH`).
4. It must deduplicate records so that for any given hour and locale, a specific translated string only appears once.
5. It should write the resulting records to `/home/user/hourly_unique_translations.txt` in the format: `YYYY-MM-DDTHH|locale|translated_text`.
6. The output file must be sorted alphabetically (which will order it by hour, then locale, then text). 
7. Compile your Rust program to an executable located exactly at `/home/user/dedup`.
8. Execute your compiled program once so that `/home/user/hourly_unique_translations.txt` is generated.
9. Finally, schedule this executable to run automatically at the top of every hour (minute 0) by adding it to the `user`'s crontab.

Ensure your Rust program correctly handles multi-byte Unicode characters, as the translation strings contain various languages.