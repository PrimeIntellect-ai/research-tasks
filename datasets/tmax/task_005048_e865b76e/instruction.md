You are an automation specialist tasked with building a resilient data processing pipeline node. Your system consists of three locally running services that have already been started by a setup script:
1. An FTP server hosting incoming data files (ftp://127.0.0.1:2121/data/).
2. A Redis server used for tracking pipeline DAG state (127.0.0.1:6379).
3. A downstream HTTP Webhook service (http://127.0.0.1:5000/webhook) expecting clean, processed data.

The data files on the FTP server are text files provided in a variety of character encodings (e.g., UTF-8, UTF-16LE, Shift-JIS, CP1252). Some of these files are clean data, while others are "evil" files containing malicious payloads (like `<script>` tags or SQL injection strings like `DROP TABLE` or `UNION SELECT`) deliberately obscured by different text encodings.

Your task is to create a Python script at `/home/user/filter_pipeline.py` that performs the following end-to-end workflow:
1. **Transfer**: Fetch all files from the FTP server's `/data/` directory.
2. **Decode**: Dynamically detect or gracefully handle the character encoding of each file, converting the content to a standard UTF-8 string.
3. **Filter**: Inspect the decoded UTF-8 string. If it contains the case-insensitive substring `<script`, `DROP TABLE`, or `UNION SELECT`, you must REJECT the file. Otherwise, ACCEPT it.
4. **Orchestrate**: For every file processed, push a JSON string to the Redis list `pipeline:results` in the format: `{"filename": "...", "status": "ACCEPTED"}` or `{"status": "REJECTED"}`.
5. **Output**: Save the accepted files to the local directory `/home/user/processed/` using the exact same filename, encoded in UTF-8. 
6. **Forward**: For accepted files, send a POST request to `http://127.0.0.1:5000/webhook` with the file's UTF-8 content as the raw body.

Ensure your script handles network transfers robustly. Run your script to process the initial batch of files already present on the FTP server.