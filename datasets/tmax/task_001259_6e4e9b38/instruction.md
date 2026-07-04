I need you to automate the provisioning of a custom log processing pipeline. As an infrastructure engineer, I am handing off a legacy process that requires a multi-stage setup. You must use standard shell tools and C for the implementation.

First, there is a screen recording of the legacy dashboard located at `/app/dashboard_recording.mp4`. You must extract the frames from this video (using `ffmpeg`) and inspect them to find the hidden `RATE_LIMIT` configuration value displayed briefly in the video.

Next, set up a bare Git repository at `/home/user/processor.git`. Configure a `post-receive` git hook so that pushing to this repository automatically:
1. Checks out the code to `/home/user/deploy`.
2. Compiles the C program (`processor.c`) into an executable named `processor`.
3. Restarts a supervisor process that manages this executable.

Write the C program `processor.c` and commit it to the git repository. The program must:
- Accept exactly one command-line argument (a log string).
- If the string starts with the exact prefix `[DEBUG]`, it should print nothing and exit with code 0.
- If the string contains the exact substring `PANIC`, it should print nothing and exit with code 1.
- Otherwise, it must print the original string, followed exactly by the suffix `_RLIMIT<VALUE>`, where `<VALUE>` is the integer you extracted from the video (e.g., `_RLIMIT42`), and exit with code 0.
- Be perfectly robust against arbitrary ASCII input strings.

Create a bash script at `/home/user/deploy/supervisor.sh` that acts as a process supervisor. When run, it should configure the local environment timezone to `Etc/UTC` and locale to `C.UTF-8`. It should then continuously run the `processor` binary, appending its standard output and standard error to `/home/user/logs/processor.log`. If the `processor` binary is updated via the git hook, the supervisor must seamlessly restart or use the new binary for subsequent invocations.

Finally, configure a log rotation policy. Create a configuration file at `/home/user/deploy/logrotate.conf` that rotates `/home/user/logs/processor.log` daily, keeps 7 backups, compresses old logs, and ensures the log file is never larger than 5MB. 

Verify your setup by pushing your C code to the git repository and ensuring the git hook correctly compiles the code, restarts the supervisor, and the log configuration is in place.