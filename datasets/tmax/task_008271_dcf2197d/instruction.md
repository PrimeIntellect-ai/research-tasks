You are a cloud architect migrating an older application's automated reports to a new secure archival server. The source server was incorrectly running in the `America/Los_Angeles` timezone, so all the backup timestamps reflect that local time instead of UTC.

You have been provided with a backup archive at `/home/user/reports_backup.tar.gz`.

Your task is to restore these files, normalize their timezone to UTC, and securely serve them over a simple local HTTPS web server. 

Complete the following steps:
1. **Restore Backup:** Extract the contents of `/home/user/reports_backup.tar.gz` into the directory `/home/user/archive_web/`.
2. **Timezone Normalization:** The extracted files follow the naming convention `report_YYYYMMDD_HHMMSS.dat` (representing `America/Los_Angeles` local time). Write and execute a Python script at `/home/user/tz_rename.py` that parses these filenames, converts the timestamp to UTC taking into account Daylight Saving Time (DST) for the respective dates, and renames the files to the format `report_YYYYMMDD_HHMMSS_UTC.dat`. 
   *(Note: Use Python's built-in `zoneinfo` and `datetime` modules).*
3. **TLS Configuration:** Generate a self-signed ECDSA (prime256v1) TLS certificate and private key. Save the certificate to `/home/user/tls.crt` and the key to `/home/user/tls.key`. The certificate should have a Common Name (CN) of `migration.local` and be valid for 30 days.
4. **Secure Web Server:** Write a Python script at `/home/user/serve.py` that uses `http.server` and the `ssl` module to serve the `/home/user/archive_web/` directory over HTTPS on `0.0.0.0:8443` using the certificate and key you generated.
5. **Start Service:** Run your `serve.py` web server in the background. Write the process ID (PID) of the web server to the file `/home/user/server.pid`.

Ensure that the web server remains running in the background upon completion.