You are acting as a localization engineer handling a broken ETL pipeline. An upstream system that synchronizes translated UI text has been experiencing retry loops, causing duplicate consecutive translations and occasionally corrupting the synchronization timestamps. 

Additionally, we have a video capture of the UI automation suite running these translations, which contains visual artifacts (pure black frames) during the moments the ETL job retried.

You need to perform a two-part task:

**Part 1: Video Analysis**
There is a video at `/app/ui_walkthrough.mp4`. During the ETL retry loops, the video drops to pure black frames (RGB: 0,0,0). 
1. Use `ffmpeg` and other shell utilities to analyze this video.
2. Identify the 0-indexed frame numbers of all pure black frames.
3. Write these frame numbers to `/home/user/glitch_frames.txt`, one number per line in ascending order.

**Part 2: Localization Data Processor (C implementation)**
You must write a robust stream processor in C (`/home/user/process_loc.c`) that reads pipe-delimited localization logs from standard input and writes cleaned data to standard output. Compile your program to `/home/user/process_loc`.

Input records are separated by standard UNIX newlines (`\n`). Maximum line length is 1024 characters.
Expected format: `timestamp|translator_email|translation_key|translated_text`

Your C program must apply the following ETL transformations:
1. **Constraint-based Validation**: Ensure the `timestamp` strictly matches the ISO-8601 format: `YYYY-MM-DDThh:mm:ssZ`. Ensure there are exactly 4 pipe-delimited fields. If a line is malformed, output `INVALID_RECORD` and skip further processing for that line.
2. **Data Masking (Anonymization)**: Mask the `translator_email`. Keep the first and last character of the local part (before the `@`), and replace everything in between with exactly three asterisks (`***`). The domain part must remain unchanged. (e.g., `john.doe@loc.com` becomes `j***e@loc.com`). If the local part is 2 characters or fewer, do not mask it.
3. **ETL Deduplication**: If a valid record has the exact same `translation_key` as the *immediately preceding valid record*, treat it as a retry duplicate. Do not output this record.
4. **Clean Output**: For all valid, non-duplicate records, output the transformed line: `timestamp|masked_email|translation_key|translated_text`.
5. **Summary Statistics**: Upon reaching EOF, print a final summary line exactly formatted as:
   `STATS: Valid=[N], Duplicates=[M]`
   Where `[N]` is the total number of valid (well-formatted), non-duplicate records printed, and `[M]` is the total number of consecutive duplicates dropped.

*Note: Your compiled binary will be heavily fuzzed against a secret reference implementation to guarantee bit-exact output for a wide range of valid and invalid byte streams.*