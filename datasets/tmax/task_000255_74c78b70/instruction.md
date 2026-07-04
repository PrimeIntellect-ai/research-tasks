You are a Data Engineer tasked with building a text processing ETL pipeline to handle customer support chat logs. 

We have a raw log file located at `/home/user/raw_chat.log`. You need to write a Python script at `/home/user/etl_pipeline.py` and run it to process this file into a clean, aggregated JSON Lines format.

**Input Format:**
The file `/home/user/raw_chat.log` contains pipe-separated values. Each line follows this format:
`DD-MMM-YYYY HH:MM:SS OFFSET | USER_ID | MESSAGE`
Example: `25-Oct-2023 14:15:00 -0700 | U001 | Contact me at alice.smith@email.com`

**Pipeline Requirements:**

1. **Timestamp Alignment & Parsing:**
   Parse the timestamps and convert them to UTC. 

2. **Data Masking (Anonymization):**
   Before aggregating, you must anonymize PII in the `MESSAGE` field:
   - **Emails:** Replace the local part (everything before `@`) with `***`. Example: `alice.smith@email.com` becomes `***@email.com`.
   - **US Phone Numbers:** Match patterns like `XXX-XXX-XXXX` (where X is a digit). Replace the first two groups with `XXX`. Example: `555-123-4567` becomes `XXX-XXX-4567`.

3. **Windowed Aggregation:**
   Group the logs into **1-hour tumbling windows** based on their **UTC** timestamps. A window starting at `14:00:00` includes all events up to, but not including, `15:00:00`.
   For each 1-hour window, aggregate the data to calculate:
   - The total number of messages in the window.
   - The number of *unique* users who sent a message in the window.
   - A list of all masked messages in chronological order.

4. **Output Format:**
   Save the results to `/home/user/processed_logs.jsonl`. Each line must be a valid JSON object representing one window, sorted chronologically by window start time. Windows with 0 messages should be omitted.
   
   Schema for each JSON line:
   ```json
   {
     "window_start": "YYYY-MM-DDTHH:00:00Z",
     "total_messages": 2,
     "unique_users": 2,
     "messages": [
       "Contact me at ***@email.com",
       "Call XXX-XXX-4567."
     ]
   }
   ```

You may use standard Python libraries. If you need third-party libraries like `pandas`, you can create a virtual environment and install them.

Execute your script so that `/home/user/processed_logs.jsonl` is created with the correct data.