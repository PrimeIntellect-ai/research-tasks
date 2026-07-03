You are a FinOps Analyst tasked with optimizing cloud storage costs. You've received an automated billing alert voicemail, but the system is currently down, so you only have the raw audio file. 

Your objectives are to parse the voicemail, identify cold storage candidates, back them up, and expose a reporting service for the auditing team.

Step 1: Analyze the Alert
There is an audio file located at `/app/billing_voicemail.wav`. Transcribe this audio file. The voicemail will dictate two critical pieces of information:
- The age threshold (in days) for classifying files as "cold" storage.
- A secret authentication token required for the reporting API.

Step 2: Storage Monitoring & Backup
You have a simulated cloud storage directory at `/home/user/cloud_data/`. 
- Identify all files in this directory (and subdirectories) that are older than the threshold specified in the audio file.
- Calculate the total size in bytes of these cold files.
- Recreate the exact directory structure of these cold files under `/home/user/archive_staging/` and move the cold files there.
- Create a compressed tarball of the staged files at `/home/user/cold_storage.tar.gz`.

Step 3: Mount Configuration
Create a configuration file at `/home/user/fstab_addition`. This file must contain exactly one line representing an fstab entry to mount a remote NFS server for long-term storage. The entry should mount `cold-vault.internal:/data` to `/mnt/archive` using the `nfs` filesystem type, with options `defaults,ro`, and dump/pass values of `0 0`.

Step 4: Reporting Service
Write a Bash script (using tools like `nc`, `socat`, or similar) that runs an HTTP server on `127.0.0.1:8080`. 
- The server must listen for `GET /report` requests.
- It must enforce authentication by checking for the HTTP header: `Authorization: Bearer <TOKEN>` (using the token extracted from the voicemail).
- If the token is missing or incorrect, return a `401 Unauthorized` HTTP response.
- If the token is valid, return a `200 OK` response with a JSON body exactly like this:
  `{"archived_files_count": X, "archived_bytes": Y, "status": "optimized"}`
  (where X is the number of files moved, and Y is the exact total size in bytes of those files).

Ensure your server runs in the background and is active when you complete your turn.