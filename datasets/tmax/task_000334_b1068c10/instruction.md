Write a Python script `/home/user/sanitiser.py` that processes a stream of configuration file updates and strictly filters out malicious or corrupted entries injected during a log rotation race condition.

Background:
You are acting as a configuration manager tracking changes. A logging service records a screencast of the system state during configuration updates. We have recovered a video trace of a log rotation race at `/app/rotation_trace.mp4`. You also have an archive of backup configurations at `/app/backups.tar.gz`.

Requirements:
1. Video Analysis: Process the video at `/app/rotation_trace.mp4`. At exactly 4 seconds into the video, the console flashes the expected metadata timestamp (format: `TIMESTAMP=YYYY-MM-DD_HH-MM-SS`) of the *valid* baseline configuration. 
2. Archive Integrity: Locate the baseline configuration file inside `/app/backups.tar.gz` that matches the recovered timestamp in its filename. Verify its integrity (it must be a valid, readable config file without standard stream redirection operators like `>`, `<`, `|`, `>>` or `&>`).
3. The Sanitiser Script: Create `/home/user/sanitiser.py`. It must accept a directory path as a command-line argument (e.g., `python /home/user/sanitiser.py /path/to/configs`).
   - The script must iterate over all `.conf` files in the given directory.
   - It must REJECT any file that:
     a) Contains standard stream redirection or piping characters anywhere in the configuration values.
     b) Attempt to reference files outside the standard `/var/log/` or `/etc/app/` paths.
     c) Fails basic metadata constraints (e.g., file size > 1MB, or has executable permissions).
   - It must PRESERVE unchanged any file that passes these checks.
   - The script must output a JSON dictionary to stdout where keys are filenames and values are either `"ACCEPTED"` or `"REJECTED"`.

We will evaluate your script by running it against a hidden evaluation suite comprising an adversarial corpus and a clean corpus. Your script must reject 100% of the evil corpus and accept 100% of the clean corpus.