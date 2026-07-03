You are an edge computing engineer deploying an anomaly detection system to an IoT device. The device records acoustic data from industrial machinery.

Your task is to build a high-performance audio processing pipeline in C, configure its deployment, manage its logs, and serve the results securely over a local web server.

**Step 1: Environment & Configuration Setup**
Create the following directories in `/home/user`: `src`, `bin`, `logs`, `www`, `tls`, `config`.
Create a configuration file `/home/user/config/sensor.conf` with the following contents:
```ini
THRESHOLD=12000
MIN_DURATION_S=0.05
LOGFILE=/home/user/logs/sensor.log
```

**Step 2: The C Processor**
Write a C program at `/home/user/src/processor.c`. This program must:
1. Parse `/home/user/config/sensor.conf` to read the configuration values.
2. Read the audio file located at `/app/machine_audio.wav` (format: 16-bit signed PCM, Mono, 44100 Hz).
3. Scan the audio for anomaly "events". An event triggers when the absolute amplitude of the audio samples equals or exceeds `THRESHOLD` for a continuous duration of at least `MIN_DURATION_S` (e.g., 0.05 seconds = 2205 samples). The event ends when the amplitude stays strictly below `THRESHOLD` for a continuous duration of `MIN_DURATION_S`. 
4. Write the results to `/home/user/www/events.csv` with the header: `event_id,start_time,duration` (times in seconds, formatted to 3 decimal places).
5. Append a log entry to `LOGFILE` for each event detected in the format: `[YYYY-MM-DD HH:MM:SS] Event <id> detected at <start_time>s for <duration>s`.

**Step 3: Log Rotation**
Create a logrotate configuration file at `/home/user/config/logrotate.conf` that targets `/home/user/logs/sensor.log`. It should rotate daily, keep 7 days of logs, and compress old logs. (You do not need to start the cron job, just provide the valid config).

**Step 4: Staged Deployment Script**
Write a bash script `/home/user/deploy.sh` that:
1. Compiles `/home/user/src/processor.c` with `gcc` (with `-O3`).
2. Backs up the existing `/home/user/bin/processor` to `/home/user/bin/processor.bak` (if it exists).
3. Moves the new compiled binary to `/home/user/bin/processor`.
4. Executes `/home/user/bin/processor`.
Make sure the script is executable and run it to generate the `events.csv`.

**Step 5: Secure Web Server**
Generate a self-signed TLS certificate (`cert.pem`) and key (`key.pem`) in `/home/user/tls/`. 
Write a script `/home/user/start_server.sh` that starts a Python HTTPS web server on port `8443` serving the `/home/user/www` directory, using the generated certificate and key. Do not block the deployment script; this script should just be runnable.

Ensure your C code is highly accurate. Your output `events.csv` will be evaluated programmatically against a hidden ground-truth using an F1 score metric for detection accuracy.