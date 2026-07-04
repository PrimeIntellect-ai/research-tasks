You are an AI assistant acting as a localization engineer. Your team has received a batch of dirty subtitle translation logs from a vendor, and you need to process them into a clean, standardized format for the translation memory database.

There are three main parts to this task:

1. **Fix and Install a Vendored Tool:** 
   We rely on a specific version of `dos2unix` to handle nasty line endings from the vendor. The source code for `dos2unix-7.4.3` is provided at `/app/dos2unix-7.4.3/`. However, the build is currently broken due to a configuration error introduced by a previous engineer. You must diagnose and fix the build process (it's a Makefile issue), compile it, and ensure the `dos2unix` binary is available for your pipeline.

2. **Data Normalization Pipeline (Bash):**
   The raw vendor logs are located at `/home/user/raw_subs.txt`. You must write a Bash script at `/home/user/pipeline.sh` that processes this file. 
   - Step A: Run your newly compiled `dos2unix` on the file to strip carriage returns.
   - Step B: Extract and align the timestamps. The raw file contains timestamps in various messy formats (e.g., `[14:05:01]`, `14:05:01 PM`, `T14:05:01Z`). Your script must extract the time, normalize it to exactly `HH:MM:SS` (24-hour format), and drop the date if present.
   - Step C: Normalize the translation text. Convert all translated text to lowercase, remove leading/trailing whitespace, and remove all punctuation (commas, periods, exclamation marks, question marks).
   - Step D: Write the standardized output to `/home/user/normalized_subs.tsv` in a tab-separated format: `HH:MM:SS<TAB>normalized_text`.

3. **Pipeline Logging:**
   Your script (`/home/user/pipeline.sh`) must append status logs to `/home/user/pipeline.log`. It should log strings like `[YYYY-MM-DD HH:MM:SS] Started processing` and `[YYYY-MM-DD HH:MM:SS] Completed dos2unix`. 

Run your script to produce `/home/user/normalized_subs.tsv`. We will automatically grade your output against a golden reference. Your output does not have to be perfect, but it must achieve a high similarity score.