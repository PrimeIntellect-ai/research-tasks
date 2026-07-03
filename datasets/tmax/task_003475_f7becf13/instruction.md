I need you to build a Python-based file processing daemon that continuously organizes incoming project files. As a developer, I have various logs and data dumps dropped into a specific directory, and they need to be standardized and moved safely. 

Here are your exact instructions:

1. Create a Python script at `/home/user/organizer.py`.
2. The script must read a configuration file at `/home/user/rules.json` (you will need to create it for testing, but assume I might change it later). For your test, `rules.json` should look like this:
   `{"output_dir": "/home/user/processed", "json_extract_keys": ["id", "status"]}`
3. The script must continuously watch the directory `/home/user/incoming/` for new files. You can use the `watchdog` library or a simple polling loop (checking every 1 second). Ensure it processes existing files on startup as well.
4. If a file ends in `.json`, parse it. It will be a list of dictionaries. Extract only the keys specified in `rules.json` (`json_extract_keys`). 
5. If a file ends in `.log`, parse it as a multi-line log. The log format is:
   `[YYYY-MM-DD HH:MM:SS] LEVEL` followed by a message that may span multiple lines, ending with a line containing strictly `===`.
   You need to extract the timestamp, the level, and the full message (replace newlines in the message with a single space).
6. For both file types, transform the extracted data into CSV format (with headers: `id,status` for JSON; `timestamp,level,message` for logs).
7. Save the CSV to the directory specified in `rules.json` (`/home/user/processed/`). The output filename must be `{original_name}.processed.csv`.
8. **CRITICAL:** Use atomic writes. You must write the output to a temporary file (e.g., `.tmp` extension) inside the output directory first, and then atomically rename it to the final `.csv` filename. This prevents partial reads by downstream systems. After processing, delete the original file from `/home/user/incoming/`.

To prove it works:
1. Create the directories `/home/user/incoming` and `/home/user/processed`.
2. Create your script and the `rules.json` file.
3. Start your script in the background (e.g., `python3 /home/user/organizer.py &`).
4. Wait 2 seconds, then manually create a file `/home/user/incoming/test1.json` containing `[{"id": 1, "status": "active", "secret": "hide_me"}, {"id": 2, "status": "inactive", "secret": "hide_me"}]`.
5. Wait 2 seconds, then create a file `/home/user/incoming/test2.log` containing:
```
[2023-10-01 10:00:00] ERROR
Database connection failed.
Retrying in 5 seconds.
===
[2023-10-01 10:00:05] INFO
Connection established.
===
```
6. Wait 5 seconds to ensure the background process picks them up, writes atomically, and deletes the originals.