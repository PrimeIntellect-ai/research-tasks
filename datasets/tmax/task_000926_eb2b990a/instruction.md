You are a Database Reliability Engineer investigating a backup infrastructure incident. Our backup reporting pipeline recently failed, and we suspect corrupted metadata and a faulty SQL query are to blame.

Complete the following objectives:

1. **Audio Incident Log**: 
An engineer recorded a voice memo during the incident, located at `/app/incident_audio.wav`. Transcribe this audio (you can use available tools like `whisper` or `ffmpeg` if you wish, or write a script to process it). The audio contains critical filtering criteria for the database query.

2. **Fix the Reporting Query**:
There is a SQLite database at `/app/backups.db` containing three tables: `servers`, `backups`, and `dependencies`. 
The script `/app/generate_report.sql` contains a query meant to materialize the backup dependency graph and return the top 10 largest successful backups. However, it currently contains an implicit cross-join bug that causes it to return incorrect results. 
Rewrite the query and save it to `/home/user/fixed_report.sql`. Your fixed query must:
- Perform the correct joins between `servers`, `backups`, and `dependencies`.
- Apply a graph projection (only servers that depend on the 'core-db' server, directly or indirectly up to 2 hops).
- Apply the filtering criteria mentioned in the audio log.
- Sort the results by backup size in descending order and paginate to return exactly the top 10 records.

3. **Backup Metadata Classifier**:
We've extracted individual backup configuration files. Some contain malicious or corrupted configurations, while others are pristine.
You must write a classifier script at `/home/user/verify_backup_record.sh` (or `.py` / `.js`) that takes a single file path as an argument.
- It must exit with status code `0` for clean files.
- It must exit with status code `1` (or any non-zero) for evil/corrupted files.
To train and test your script, use the corpora provided at `/app/corpus/clean/` (contains only valid records) and `/app/corpus/evil/` (contains only corrupted records). Your solution must perfectly classify these sets.

Ensure your classifier is executable and uses the exact signature: `./verify_backup_record.sh <path_to_json>`