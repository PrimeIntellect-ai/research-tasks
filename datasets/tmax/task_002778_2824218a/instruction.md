You are acting as a data engineering assistant. I am a data scientist and I've received a massive, poorly formatted application log file. I need to extract structured data from it to insert into our database, but the file is too large to load into memory all at once.

The log file is located at `/home/user/app_dirty.log`.

Your task is to write and execute a Python script `/home/user/process_logs.py` that processes this log file.

Requirements:
1. **Large-file streaming:** Your script must read `/home/user/app_dirty.log` line-by-line. Do not load the entire file into memory (e.g., do not use `.read()` or `.readlines()`).
2. **Regex pattern construction:** For each line, attempt to extract:
   - A timestamp in the exact format `YYYY-MM-DD HH:MM:SS`
   - An IPv4 address
   - An email address
   If a line does not contain all three of these elements, skip it.
3. **Template-based text generation:** For the lines that do match, use string formatting/templating to generate a SQL INSERT statement exactly matching this format:
   `INSERT INTO user_activity (event_time, ip_address, user_email) VALUES ('<timestamp>', '<ip>', '<email>');`
4. **Output:** Write the generated SQL statements to `/home/user/clean_inserts.sql`, one statement per line.

Ensure the final `.sql` file is properly formatted and contains only the valid inserts. You must run your script so that the output file is generated.