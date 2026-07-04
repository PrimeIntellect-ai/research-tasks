You are a data analyst working with multilingual user feedback. You have received a raw CSV file at `/home/user/feedback.csv` containing user reports. Unfortunately, the system that exported this data corrupted the text by leaving Unicode characters as raw escape sequences (e.g., `\u00e9` instead of `é`), and you need to build a C++ data processing pipeline to clean, filter, and sample it.

Write a C++ program at `/home/user/process.cpp` (and compile it to `/home/user/process`) that does the following:

1. **Read the CSV**: Read `/home/user/feedback.csv`. The file has three columns: `id`, `region`, and `feedback` (separated by commas).
2. **Character Encoding Handling**: Parse the `feedback` column and decode any `\uXXXX` sequences into valid UTF-8 characters. For example, `\u00e9` should become `é`, and `\u26a0` should become `⚠`. (Assume `XXXX` is exactly 4 hex digits).
3. **Regex Pattern Construction**: Filter the rows. Keep only the rows where the *decoded* `feedback` text contains any of the following keywords (case-insensitive): `error`, `bug`, or `fail`. 
4. **Data Sampling and Stratification**: From the filtered matching records, perform a deterministic stratified sample: extract exactly the *first 2* matching records for each `region`, based on their original order in the file. If a region has fewer than 2 matches, keep whatever matches exist.
5. **Output**: Write the sampled, decoded records to `/home/user/sampled_bugs.csv`. Include the header `id,region,feedback`.
6. **Pipeline Logging**: Write a log file to `/home/user/pipeline.log` strictly in the following format:
   ```
   TOTAL_ROWS: <total data rows processed, excluding header>
   MATCHED_BUGS: <total rows matching the regex>
   SAMPLED_RECORDS: <total rows outputted after stratification>
   ```

**Constraints:**
* Use C++17 or later (`g++ -std=c++17 process.cpp -o process`).
* You may use standard C++ libraries, including `<regex>`.
* Ensure output CSV formatting matches standard expectations (no unescaped commas inside the feedback string for this dataset).