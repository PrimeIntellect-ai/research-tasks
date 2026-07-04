You are an automation specialist setting up a daily pipeline to process multi-lingual chat logs. 

We receive a raw log file at `/home/user/data/chats.txt`. The file uses a pipe-separated format:
`UnixTimestamp|LanguageCode|Message`

The messages are in UTF-8 and contain various languages and emojis.

Your task is to write a C++ program that processes this data, compiles it, and schedules it.

**Step 1: Write the C++ Processor**
Create a C++ program at `/home/user/process.cpp`.
The program must:
1. Read `/home/user/data/chats.txt`.
2. Group the records into 1-hour time buckets. (An hour bucket is the Unix timestamp rounded down to the nearest multiple of 3600. For example, timestamp `3615` belongs to bucket `3600`).
3. Within each hour bucket, deduplicate the records. Keep only the *first* occurrence of each unique `LanguageCode|Message` combination. (Do not modify or normalize the UTF-8 messages, just use exact string matching).
4. Output the deduplicated records to `/home/user/output/deduped.tsv`.
5. The output format must be tab-separated: `HourBucket\tLanguageCode\tMessage`.
6. Maintain the chronological order of the first occurrence of each retained message.

**Step 2: Compile**
Compile your program to an executable at `/home/user/process` using `g++ -std=c++17 -O2 /home/user/process.cpp -o /home/user/process`.

**Step 3: Schedule**
Create a cron configuration file at `/home/user/mycron` that schedules `/home/user/process` to run automatically at exactly 2:00 AM every day. The file should contain a single valid crontab line. 
*(Note: You do not need to install it via `crontab /home/user/mycron`, just create the text file with the correct expression).*

**Constraints & Notes:**
- Handle file paths strictly as given.
- Create `/home/user/output/` directory if it does not exist.
- Assume inputs are well-formed UTF-8. 
- You may use standard C++ libraries (`<iostream>`, `<fstream>`, `<string>`, `<unordered_set>`, `<vector>`, etc.).