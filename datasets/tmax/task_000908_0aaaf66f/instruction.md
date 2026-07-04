You are a log analyst investigating a critical customer support anomaly. A sophisticated log-injection attack has been detected in the system, and previous naïve bash scripts used to process logs have been failing because they silently drop rows containing properly quoted embedded newlines, or worse, they allow log injection payloads through.

Your investigation requires completing the following multi-stage workflow exclusively using Bash, shell built-ins, and standard Unix utilities (like `awk`, `sed`, `grep`). Do not use Python, Perl, or Ruby.

**Stage 1: Audio Extraction**
An automated system left a voicemail containing the exact Incident ID you need to investigate.
- The audio file is located at `/app/voicemail.wav`.
- Extract the spoken Incident ID from this audio (you may use available tools like `whisper-cli` or `ffmpeg` if needed, or simply listen to it if your environment permits). It will be in the format `INC-XXXX`.

**Stage 2: Build an Adversarial CSV Detector**
You must write a strict CSV filter script at `/home/user/detector.sh` that reads from standard input and writes to standard output. 
The CSV format has exactly 4 columns: `timestamp,incident_id,response_time,message`.
- **Clean data:** Valid CSV rows. Note that the `message` field is enclosed in double quotes and may contain legitimate, quoted embedded newlines.
- **Evil data:** Log injection attacks where an attacker has inserted unquoted newlines and fake timestamps to forge secondary log entries.
Your script must output *only* valid, properly formatted log records. It must correctly parse multi-line quoted fields without dropping them, and it must completely drop any forged/malformed rows.

**Stage 3: Streaming Analysis & Imputation**
The main log file is located at `/app/raw_logs.csv`.
1. Stream `/app/raw_logs.csv` through your `/home/user/detector.sh`.
2. Filter the sanitized output to include ONLY the rows matching the Incident ID you discovered in Stage 1.
3. The `response_time` column (column 3) occasionally has missing (empty) values. You must impute these missing values using **forward-fill** (replace an empty value with the most recently observed valid `response_time` for this incident).
4. Calculate a **rolling average of the last 3** `response_time` values (including imputed ones). For the first two rows, the rolling average is just the average of the available 1 or 2 rows.
5. Output the final aggregated data to `/home/user/rolling_avg.csv` in the format:
`timestamp,incident_id,imputed_response_time,rolling_avg`
(Round the `rolling_avg` to exactly 2 decimal places).

Ensure your script `/home/user/detector.sh` is executable (`chmod +x`). Your pipeline relies on correctly handling quoted newlines in bash/awk, which is the primary challenge.