You are an observability engineer tuning dashboards for a custom monitoring daemon. The dashboard currently parses logs incorrectly because the daemon isn't respecting timezone or locale settings, and the log file is growing indefinitely, causing disk pressure.

We have a simple daemon written in C located at `/home/user/daemon.c`. It is supposed to print log messages with timestamps formatted according to the system's locale and timezone.

Your task is to fix the daemon, deploy it, and configure log rotation:

1. **Fix the C Code:** Modify `/home/user/daemon.c` so that it properly initializes the locale (using the environment's default) and timezone before its main loop. (Hint: look into `setlocale` and `tzset` in the `<locale.h>` and `<time.h>` headers). Compile the fixed code to `/home/user/daemon` using `gcc`.

2. **Create a Launch Script:** Create a shell script at `/home/user/start.sh` that:
   - Sets the Timezone to `Asia/Tokyo`.
   - Sets the Locale (`LC_ALL`) to `ja_JP.UTF-8`.
   - Starts the compiled `/home/user/daemon` in the background.
   - Redirects standard output to `/home/user/daemon.log`.
   - Make sure the script is executable.

3. **Configure Log Rotation:** Create a logrotate configuration file at `/home/user/logrotate.conf` designed to run in user-space. It must target `/home/user/daemon.log` and specify the following rules:
   - Rotate daily.
   - Keep exactly 3 rotated backups.
   - Compress the rotated files.
   - Missing log files should not generate an error (missingok).

Do not actually run `logrotate` or the daemon daemon—just create the compiled binary, the launch script, and the configuration file.