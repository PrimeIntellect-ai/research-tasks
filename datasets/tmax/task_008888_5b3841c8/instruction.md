You are a monitoring specialist for a cluster. Users have been complaining that their automated jobs are silently failing. You suspect they are hitting their storage quotas, but the current monitoring system is broken and silently rejecting alerts.

Your task is to write a custom Rust monitoring tool that checks simulated mount points, maps them to users, and generates an alert log for anyone exceeding their quota.

Here is the setup. The system configuration is simulated in your home directory:

1. **`/home/user/custom_fstab`**: Contains the simulated mount configuration.
   Format: `<device> <mount_point> <fstype> <options> <dump> <pass>`
   Example line: `/dev/loop1 /home/user/storage/alice_data ext4 rw,uid=1001,quota=50000 0 0`
   The `options` field contains a comma-separated list. You need to extract the `uid` and the `quota` (which is the maximum allowed size in bytes).

2. **`/home/user/mock_passwd`**: Contains user account information (standard `/etc/passwd` format).
   Format: `username:password:UID:GID:GECOS:directory:shell`
   You need to use this to map the `uid` found in the custom fstab to a `username`.

3. **`/home/user/storage/`**: This directory contains the simulated mount points. Each user's mount point (as specified in the fstab) contains exactly one file named `data.bin`. The actual storage usage for a mount point is the exact file size of `data.bin` in bytes.

**Your Objective:**
1. Create a Rust project named `quota_monitor` in `/home/user/`.
2. Write a Rust program that reads the above configurations, calculates the exact size of `data.bin` in each user's mount point, and checks if it exceeds their assigned `quota`.
3. For every user whose usage is **strictly greater** than their quota limit, append a line to `/home/user/quota_alerts.log` in the exact following format:
   `ALERT: User <username> exceeded quota on <mount_point>. Usage: <usage> bytes, Limit: <limit> bytes.`
4. Compile and run your Rust program so that `/home/user/quota_alerts.log` is generated. Sort the log entries alphabetically by username.

Constraints:
- You must write the solution in Rust. You can use standard standard library features.
- Do not use external crates except those available by default in standard Rust.
- Make sure to handle parsing robustly.