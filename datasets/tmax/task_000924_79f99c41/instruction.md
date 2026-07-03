You are an automation specialist tasked with creating a data extraction and reporting pipeline. 

You have been provided with a large raw log file at `/home/user/raw_logs.txt`. This file contains millions of lines of mixed system output. Your goal is to stream this large file, extract specific structured data using regex, perform a stratified sampling based on error codes, and generate a final report using a provided template.

Here are the exact requirements:

1. **Information Extraction via Regex:**
   You must scan `/home/user/raw_logs.txt`. Valid log entries are single lines that strictly match this format:
   `[YYYY-MM-DD HH:MM:SS] [<LEVEL>] [UID:<user_id>] Action <action_name> resulted in code <code>. Latency: <latency>ms. Msg: <message>`
   
   - `<LEVEL>` can be INFO, WARN, or ERROR.
   - `<user_id>` is an alphanumeric string.
   - `<action_name>` is an uppercase alphabetic string (e.g., LOGIN, QUERY).
   - `<code>` is a 3-digit integer.
   - `<latency>` is an integer representing milliseconds.
   - `<message>` is any remaining text to the end of the line.
   
   *Note: The file contains many "junk" lines that do not match this format. Ignore them.*

2. **Stratified Sampling:**
   You must group the valid extracted log entries by their 3-digit `<code>`. 
   For each unique `<code>`, you must select exactly the **top 3** log entries with the **highest `<latency>`**. 
   If a code has fewer than 3 valid entries, select all of them. If there is a tie in latency, preserve the order of appearance in the file.
   *Performance note: Since the file is large, process it iteratively (streaming) keeping only the top 3 per code in memory, rather than loading the whole file.*

3. **Template-Based Generation:**
   You have a template file at `/home/user/report_template.md`.
   Using your stratified sample, generate a final report at `/home/user/final_report.md`.
   
   Your generated report must exactly follow this markdown structure:
   
   ```markdown
   # System Latency and Status Report
   
   ## Code: 200
   1. UID: A12, Action: LOGIN, Latency: 950ms
   2. UID: B34, Action: QUERY, Latency: 840ms
   3. UID: C56, Action: LOGOUT, Latency: 120ms
   
   ## Code: 404
   ...
   ```
   
   - Sort the `## Code: <code>` sections in ascending numerical order of the code.
   - Within each code section, order the top 3 entries in descending order of latency.
   - Exactly match the formatting: `UID: <user_id>, Action: <action_name>, Latency: <latency>ms`

Write a script (Python, Bash, or a mix) to automate this workflow and generate `/home/user/final_report.md`.