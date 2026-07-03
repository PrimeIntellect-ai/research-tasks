You are a network engineer troubleshooting intermittent connectivity issues on a core switch. The vendor suspects that malicious log entries injected by anomalous network packets might be crashing the switch's log-parsing daemon, leading to link drops.

You have three main objectives:

**1. Video Analysis of Link Drops**
The vendor provided a diagnostic video recording of the switch's console dashboard during an outage: `/app/switch_monitor.mp4`. In this diagnostic tool, a link drop is represented by a completely red frame. 
- Use `ffmpeg` (which is preinstalled) and any standard CLI tools to extract the frames and count exactly how many completely red frames exist in the video.
- Save this exact integer count to `/home/user/drop_count.txt`.

**2. Log Classifier (Adversarial Detection)**
To prevent the daemon from crashing, you must write a strict log classifier shell script at `/home/user/log_classifier.sh`.
- The script must take a single argument: the path to a log file.
- It must read the file and determine if it is "clean" or "evil".
- A "clean" log file contains only valid, safe characters: alphanumeric (`A-Z`, `a-z`, `0-9`), spaces, hyphens (`-`), underscores (`_`), colons (`:`), periods (`.`), and square brackets (`[`, `]`).
- An "evil" log file contains malicious shell metacharacters (e.g., `;`, `|`, `&`, `$`, `<`, `>`, backticks) designed to exploit the parser.
- Your script must exit with code `0` if the file is completely clean.
- Your script must exit with code `1` if the file contains *any* characters outside the safe set.
- Ensure the script is executable.

**3. System Configuration & Backup**
To deploy this fix:
- Create a backup of the current parser configuration directory. Compress `/home/user/netmon_config/` into a tarball at `/home/user/backup.tar.gz`.
- Define a user-level systemd service to run your classifier. Create the file `/home/user/.config/systemd/user/log-filter.service`. It should be a standard systemd service unit where `ExecStart=/home/user/log_classifier.sh %f` (or similar standard systemd syntax) and the service description is "Network Log Filter".
- Add the environment variable `export FILTER_STRICT=1` to the bottom of `/home/user/.bashrc`.