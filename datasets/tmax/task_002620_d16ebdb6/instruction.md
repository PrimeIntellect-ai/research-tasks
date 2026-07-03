You are an edge computing engineer deploying a new data ingestion pipeline for IoT acoustic sensors. The devices collect ambient audio, but recently they have been targeted by malicious actors sending malformed payloads designed to crash our downstream processing systems. 

Your task is to set up a robust, automated edge filtering system on this device.

**Step 1: Extract Deployment Directive**
There is an audio file at `/app/directive.wav` containing a spoken deployment code. Extract or transcribe this code and save it exactly as a single line in `/home/user/node_code.txt`.

**Step 2: Build the C Payload Filter**
Write a C program at `/home/user/filter.c` and compile it to `/home/user/filter`. This program must take a single command-line argument: the path to a WAV file. 
It must perform strict validation of the WAV file header:
1. It must verify the "RIFF" chunk ID.
2. It must verify the "WAVE" format ID.
3. It must verify that the audio format in the "fmt " subchunk is 1 (uncompressed PCM).
4. It must verify that the declared RIFF chunk size matches the actual physical file size (allowing for an 8-byte header offset, so `RIFF_size + 8 == actual_file_size`).
If the file passes all checks, the program must exit with status `0` (clean). If it fails any check, it must exit with status `1` (evil/malformed).

You must ensure your program perfectly classifies the provided adversarial corpora:
- Clean corpus (must all exit 0): `/app/corpora/clean/`
- Evil corpus (must all exit 1): `/app/corpora/evil/`

**Step 3: Automation Pipeline**
Create a shell script at `/home/user/pipeline.sh` that processes new files. 
- It should scan `/home/user/incoming/` for any `.wav` files.
- It must run `/home/user/filter` on each file.
- If the file is clean, move it to `/home/user/approved/`.
- If the file is malicious, move it to `/home/user/rejected/`.
Ensure the script is executable. Create the necessary directories.
Configure a user-level cron job that executes `/home/user/pipeline.sh` every minute.

**Step 4: Edge Distribution Proxy**
We need to serve the approved files to downstream aggregators. 
Configure a user-space Nginx instance to serve the contents of `/home/user/approved/` over HTTP on port `8080`.
Create your configuration file at `/home/user/nginx.conf`. Ensure Nginx runs without root privileges, uses `/home/user/nginx_logs/` for access/error logs, and uses `/home/user/nginx_temp/` for temporary paths to avoid permission issues. Start the Nginx process in the background.

Ensure all services are running and scripts are executable.