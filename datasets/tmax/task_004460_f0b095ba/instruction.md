You are acting as a data engineer assisting a data scientist with cleaning a corrupted dataset. 

An upstream ETL job that extracts acoustic events from machine monitoring audio failed and retried, resulting in duplicate records. Because the retries happened with slightly misaligned temporal windows, the duplicate records have slightly shifted timestamps and variations in their metadata.

You have been provided with:
1. `/app/machine_audio.wav`: The raw 16-bit PCM Mono WAV file (sample rate 16000 Hz) containing the source audio for the ETL run.
2. `/app/noisy_events.csv`: A CSV file containing the extracted events. Format: `event_id,timestamp_ms,duration_ms,confidence_score`.

Your task is to write a C program that cleans this dataset by doing the following:
1. **Time-based Bucketing & Feature Extraction**: Parse the `/app/machine_audio.wav` file and compute the Root Mean Square (RMS) energy of the audio signal for consecutive, non-overlapping 50-millisecond time buckets.
2. **Distance and Similarity Computation**: For each record in `/app/noisy_events.csv`, calculate a feature signature based on the average RMS energy of the audio buckets that intersect with the event's time window (`timestamp_ms` to `timestamp_ms + duration_ms`).
3. **Deduplication**: Identify duplicate events. Two events are considered duplicates if their start timestamps are within 150ms of each other AND the absolute difference in their computed RMS feature signatures is less than 5.0. When duplicates are found, keep the event with the higher `confidence_score` and discard the others.
4. **Database Export**: Create a SQLite database at `/home/user/clean_events.db`. Bulk import your final deduplicated records into a table named `events` with the schema: `(event_id TEXT, timestamp_ms INTEGER, duration_ms INTEGER, confidence_score REAL)`.

Requirements:
- Your core processing, bucketing, and similarity computation MUST be implemented in C.
- You may use standard bash/Linux coreutils and `sqlite3` to orchestrate the pipeline and perform the final database import.
- Place all your source code in `/home/user/src/` and compile it there.

The final evaluation will programmatically compare your `/home/user/clean_events.db` against a ground-truth reference using an F1-score metric.