A configuration management pipeline recently experienced intermittent connection issues, causing it to retry its deployment jobs multiple times. This resulted in several near-duplicate configuration files being generated and logged. 

You need to write a Python script at `/home/user/find_duplicates.py` to identify these redundant configuration files. 

Here are the requirements:
1. Parse the pipeline log file located at `/home/user/deploy.log`. Use Regular Expressions to extract the file paths of all deployed configurations. The relevant lines look exactly like:
   `[YYYY-MM-DD HH:MM:SS] [INFO] Deployed config to /path/to/file.conf`
   (Ignore any other log levels or messages).
2. Process the extracted file paths in the exact order they appear in the log.
3. Keep track of the "unique" configuration files. For each file path extracted, read its contents and compare it against all previously identified *unique* configuration files.
4. To compare files, use Python's built-in `difflib.SequenceMatcher(None, text1, text2).ratio()`. If the similarity ratio between the current file's content and ANY previously identified unique file's content is `>= 0.90`, consider the current file a "duplicate" (it is a product of a retry). Otherwise, add it to your collection of unique files.
5. Write the absolute file paths of all identified "duplicate" configuration files to a new file at `/home/user/duplicates.log`. Write one file path per line, in the order they were discovered.

Your script must be self-contained and use only standard library modules. Once written, execute your script to produce the `/home/user/duplicates.log` file.