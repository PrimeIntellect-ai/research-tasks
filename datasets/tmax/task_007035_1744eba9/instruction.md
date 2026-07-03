You are a localization engineer analyzing translation velocities to update resource allocations. You have a raw log file of translation events in `/home/user/translation_logs.csv`.

The CSV has the following format (header included):
`timestamp,locale,words`

Example rows:
```
2023-10-01T08:00:00Z,fr-FR,150
2023-10-01T12:00:00Z,es-ES,400
```

Your task is to build a multi-stage pipeline using Rust and Bash to calculate time-series rolling aggregations for the `fr-FR` locale.

1. Write a standalone Rust program at `/home/user/process.rs` (no Cargo required, must compile with standard `rustc`).
    - Read `/home/user/translation_logs.csv`.
    - Filter the dataset to include only rows where `locale` is `fr-FR`.
    - Extract the date portion (`YYYY-MM-DD`) from the `timestamp`.
    - Calculate the total `words` translated per day.
    - Sort the aggregated data chronologically by date.
    - Compute a 3-day rolling average of the daily total words. For a given day, the rolling average is the mean of the daily totals for that day and up to two immediately preceding days *that are present in the filtered fr-FR data* (e.g., if it's the first day, divide by 1; if it's the second day, divide by 2; otherwise divide by 3).
    - Output the result to `/home/user/fr_stats.csv` with the exact header `date,daily_words,rolling_avg`. Format `rolling_avg` strictly to 2 decimal places (e.g., `250.00`).

2. Write a shell script `/home/user/pipeline.sh` that:
    - Compiles `/home/user/process.rs` using `rustc`.
    - Runs the compiled binary.
    - Parses the resulting `/home/user/fr_stats.csv` using a shell utility (like `awk` or `tail`) to extract the absolute maximum `rolling_avg` value and writes *only* that number to `/home/user/max_avg.txt`.

Ensure `/home/user/pipeline.sh` is executable and run it to produce the final artifacts.