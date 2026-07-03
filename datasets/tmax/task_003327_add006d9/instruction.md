You are an observability engineer tasked with tuning a new alerting pipeline for our monitoring dashboards. We are building a Bash-based CI/CD pipeline that processes video captures of legacy monitoring screens, generates alert emails, and routes them to our on-call system.

Your task is to build the required pipeline and filters using only Bash, standard coreutils, and ffmpeg/imagemagick.

**Step 1: Video Dashboard Processing**
We have a screen recording of the legacy dashboard at `/app/dashboard_capture.mp4`. 
Write a Bash script `/home/user/extract_alerts.sh` that:
1. Uses `ffmpeg` to extract frames at 1 frame per second into `/home/user/dashboard_frames/`.
2. Counts the total number of extracted frames and writes this integer to `/home/user/frame_count.txt`.

**Step 2: Adversarial Email Filter**
Our alert mailing list is frequently targeted by log-injection and spam attacks. You must build a sanitization filter `/home/user/alert_filter.sh` that reads an alert email text file (passed as the first argument, e.g., `./alert_filter.sh email.txt`) and exits with `0` if the email is clean, or exits with `1` if the email is malicious.
* To train and test your script, we have provided two corpora of raw email files:
  * Clean alerts: `/app/corpora/clean_alerts/`
  * Evil alerts: `/app/corpora/evil_alerts/`
* Malicious alerts in this scenario always contain injected shell commands denoted by `$(...)` or backticks `` `...` ``, or contain the exact string `DROP TABLE`. Clean alerts only contain standard alphanumeric text, standard punctuation, and JSON-formatted metric payloads.
* Your script must achieve 100% accuracy on these provided directories.

**Step 3: Network Routing Config**
Generate a simulated static routing configuration file at `/home/user/alert_routes.conf`. It must contain exactly two lines:
1. A route for the primary mail server subnet `10.50.0.0/16` via gateway `192.168.1.254`.
2. A default fallback route `0.0.0.0/0` via `192.168.1.1`.
Format: `[CIDR] via [GATEWAY]`

**Step 4: CI/CD Pipeline Integration**
Create the main pipeline script at `/home/user/pipeline.sh` that executes the video extraction, then iterates over all `.eml` files in `/app/incoming_alerts/`, runs them through your `alert_filter.sh`, and if they pass (exit 0), copies them to `/home/user/verified_maildir/new/` (create this directory structure).

Ensure all scripts are executable (`chmod +x`).