You are a data engineer tasked with fixing a broken ETL pipeline. An upstream ETL job recently crashed and automatically retried, but it failed to clear its partial output before resuming. As a result, the output data dump contains an overlapping region of records. To make matters worse, the payloads in the retried records have slight string variations (noise) compared to the original records, meaning simple deduplication won't work.

You need to write a C++ program that reads the corrupted data dump, detects the anomaly/changepoint where the job restarted, identifies the fuzzy duplicates, and outputs a clean dataset.

**Input Data Description:**
The input file is located at `/home/user/etl_dump.txt`.
Each line follows this exact format:
`[YYYY-MM-DD HH:MM:SS] JOB-<ID> | SEQ:<NUMBER> | PAYLOAD:<STRING>`

**Requirements for your C++ program:**
1. **Regex Parsing:** Use C++ `<regex>` to parse each line into its components (Timestamp, Job ID, Sequence Number, and Payload).
2. **Changepoint Detection:** The sequence numbers strictly increase by 1 for each record. The "changepoint" is the exact line where the sequence number abruptly drops (indicating the retry started). You must detect this line number (1-indexed).
3. **Similarity Computation:** After the changepoint, the job re-processed some records. A post-changepoint record is considered a "fuzzy duplicate" of a pre-changepoint record if:
   - It has the *same* Sequence Number.
   - The Levenshtein distance between their `PAYLOAD` strings is **less than or equal to 2**.
4. **Data Cleaning:** Create a cleaned output file at `/home/user/cleaned_etl.txt`. 
   - Write all pre-changepoint records exactly as they appeared.
   - For post-changepoint records, do *not* write them if they are fuzzy duplicates of any pre-changepoint record.
   - If a post-changepoint record is *not* a fuzzy duplicate (e.g., it's a completely new sequence number that wasn't reached before the crash), write it to the output file.
5. **Anomaly Reporting:** Create a JSON file at `/home/user/anomaly_report.json` with the following exact format:
   ```json
   {
       "changepoint_line": <integer>,
       "duplicates_removed": <integer>
   }
   ```
   *Note: `changepoint_line` is the 1-indexed line number in the original file where the sequence number first dropped.*

**Constraints & Execution:**
- You may install any necessary build tools (like `g++`, `cmake`) via `apt-get` or `apt` using `sudo` if needed (you have passwordless sudo). Wait, you are running in a container, assume standard package manager access is allowed, but do not rely on external C++ libraries other than the standard library (C++17 is fine). You must write the Levenshtein distance function yourself.
- Write your code to `/home/user/cleaner.cpp`.
- Compile it to `/home/user/cleaner` and execute it so that the output files are generated.