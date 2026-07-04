You are a Data Engineer tasked with building a lightweight ETL pipeline using Bash. You need to process a large-scale dataset of transcribed audio records, filter out corrupt or anomalous records, and extract metadata from raw audio files. 

Your tasks are to:

1. **Audio Metadata Extraction (Outlier detection setup):**
   You have a raw audio file located at `/app/interview.wav`. In our pipeline, we need to know the exact duration of raw audio files to establish outlier boundaries.
   Use `ffprobe` (or `ffmpeg`) to extract the precise duration of this audio file in seconds.
   Write the duration (just the number, exactly as output by ffprobe) to `/home/user/audio_duration.txt`.

2. **ETL Record Sanitizer (Adversarial Filtering):**
   Our transcription pipeline outputs individual records as JSON files. Many of these records contain missing values, hallucinated transcripts, or duration outliers.
   
   Write a Bash script at `/home/user/validate_record.sh`.
   The script must take a single argument: the path to a JSON file.
   It must output exit code `0` if the record is CLEAN, and exit code `1` if the record is EVIL (corrupted/anomalous).

   A JSON file is considered EVIL if **any** of the following are true:
   - **Missing Values:** The `speaker` field is missing, empty (`""`), or explicitly `null`.
   - **Outliers:** The `duration` field is less than `1.0` or greater than `100.0` (it must be numeric).
   - **Similarity/Spam Detection:** The `transcript` field contains the exact phrase `"Thank you for watching"` or `"Subtitles by"` (case-insensitive).
   
   A JSON file is CLEAN if it possesses a valid `speaker`, a valid `duration` between 1.0 and 100.0 inclusive, and does not contain the spam phrases in its `transcript`.

   *Constraints:*
   - You must use Bash and standard utilities (like `jq`, `grep`, `awk`).
   - The script must be executable (`chmod +x`).
   - It should not print anything to stdout/stderr, only return the correct exit code.

Ensure your script is robust, as it will be evaluated against thousands of clean and evil edge-case files in our hidden test suites.