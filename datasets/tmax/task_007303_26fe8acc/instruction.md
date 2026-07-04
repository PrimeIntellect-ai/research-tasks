You are a monitoring specialist setting up an out-of-hours alert system for a local Git repository.

A bare Git repository exists at `/home/user/monitor.git`. You need to configure a Git hook and a Python script to monitor incoming pushes and log an alert if a commit was authored during "off-hours" in a specific timezone.

Perform the following steps:

1. **Git Hook Setup**: Create a `post-receive` hook in `/home/user/monitor.git/hooks/post-receive`. Ensure it is executable. This hook must capture the standard input provided by Git (which contains `oldrev newrev refname`) and pass it to a Python script located at `/home/user/alert_check.py`.

2. **Python Alert Dispatcher**: Write the Python script `/home/user/alert_check.py`. For each reference updated (read from standard input), the script must:
   - Extract the Unix timestamp of the newly pushed commit (`newrev`). You can use a subprocess to call `git show -s --format=%ct <newrev>` inside the `/home/user/monitor.git` directory.
   - Convert this Unix timestamp to the `Asia/Tokyo` timezone.
   - Extract the hour of the day in `Asia/Tokyo` (0-23).
   - "Off-hours" are defined as any hour from `22` (10 PM) to `05` (5 AM) inclusive. 
   - If the commit's `Asia/Tokyo` hour falls within the off-hours, the script must trigger an alert.

3. **Routing Information**: As part of the alert, the script needs to know which network interface handles the default outbound route. The script must execute `ip route`, find the line starting with `default`, and extract the associated interface name (e.g., `eth0`, `ens3`, etc., immediately following the `dev` keyword).

4. **Alert Logging and Permissions**:
   - For any off-hours commit, append exactly one line to `/home/user/alerts.log` in the following format:
     `ALERT: commit=<newrev> tz_hour=<hour> iface=<interface_name>`
     (e.g., `ALERT: commit=1a2b3c... tz_hour=23 iface=eth0`)
   - Ensure that `/home/user/alerts.log` has strict permissions of `600` (read and write only by the owner). The script should enforce this permission either upon creating the file or after writing to it.

Make sure your Python script cleanly handles the input formats and dependencies. Do not use external Python libraries that require `pip install` (standard library `datetime`, `zoneinfo`, `subprocess`, `sys`, `os` are fine).