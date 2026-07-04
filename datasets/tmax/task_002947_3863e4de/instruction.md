You are an operations engineer triaging a critical incident in a data ingestion pipeline. The reporting service has crashed, and the telemetry database appears to be corrupted following a hard server crash.

Your objectives are:
1. **Database Recovery:** The SQLite database located at `/home/user/telemetry.db` is throwing "database disk image is malformed" errors. Recover the data into a new database file at `/home/user/telemetry_recovered.db`. 
2. **Encoding/Serialization Troubleshooting:** The processing script at `/home/user/triage.py` reads a `payload` BLOB column from the database, which contains JSON data. The script currently crashes with a `UnicodeDecodeError` because some legacy sensors transmitted their payloads in `latin-1` instead of `utf-8`. Modify `/home/user/triage.py` to read from the newly recovered database and gracefully handle the decoding (if `utf-8` fails, fall back to `latin-1`).
3. **Statistical Anomaly Investigation:** Once the data is successfully decoded, the script parses the JSON (which contains a `temp` field). There are statistical anomalies in the temperature data caused by failing sensors. Modify the script to identify all database `id`s where the temperature exceeds the mean temperature of all validly parsed records by more than 3 standard deviations (Z-score > 3). 

Write the isolated anomalous `id`s (sorted in ascending numerical order, one per line) to `/home/user/anomalies.txt`.

Ensure your updated `/home/user/triage.py` can be executed directly without errors and successfully writes the `/home/user/anomalies.txt` file.