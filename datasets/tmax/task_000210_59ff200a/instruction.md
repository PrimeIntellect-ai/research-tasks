You are tasked with building a configuration management data pipeline that processes both physical server monitoring data and software configuration backups.

**Part 1: Video Alert Extraction**
An edge server's status camera has captured a video of the hardware LED indicators, located at `/app/server_leds.mp4`. 
You need to analyze this video to detect hardware error states.
1. Extract the frames of the video using `ffmpeg` or Python (e.g., OpenCV, which you may need to install).
2. Analyze each frame. A "hardware error" frame is defined as any frame where the average color of the top-left 20x20 pixel region is predominantly red (specifically: Average Red channel > 150, Average Green channel < 100, and Average Blue channel < 100).
3. Count the total number of hardware error frames and write this single integer to `/home/user/red_alert_count.txt`.

**Part 2: Configuration Sanitizer**
We receive JSON configuration backups from edge devices. Unfortunately, some configurations are maliciously modified or corrupted.
You must create a Python script at `/home/user/verify_config.py` that takes a single file path as a command-line argument and validates the configuration.
The script must exit with status `0` if the configuration is safe/valid, and exit with status `1` if it is malicious/invalid.
Validation rules:
- The file must be valid parseable JSON.
- If the JSON contains a `"users"` key (which is a list of objects), no user object may have `"privilege": "root"` unless their `"username"` is exactly `"admin"`. Any other username with root privileges is an unauthorized backdoor.
- The `"hostname"` string (if present) must consist strictly of alphanumeric characters and hyphens (no spaces, shell metacharacters, or symbols).

**Part 3: ETL and Database Import**
You are provided with a directory of incoming JSON configuration files at `/app/incoming_configs/`.
1. Stream and iterate through all `.json` files in this directory.
2. Use your `/home/user/verify_config.py` logic to filter out malicious/invalid files.
3. For all valid configurations, normalize the data by extracting the `"hostname"`, `"ip_address"`, and `"timestamp"`.
4. Bulk insert these records into a SQLite database located at `/home/user/cmdb.db` in a table named `valid_configs` with columns: `hostname` (TEXT), `ip_address` (TEXT), and `timestamp` (INTEGER). 
Ensure the database and table are created if they do not exist.