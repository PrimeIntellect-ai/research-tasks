You are assisting a cloud architect with migrating a legacy Git-based configuration management system. The previous administrator left behind an audio voicemail with some crucial missing context, a compiled legacy binary that needs to be rewritten in Rust, and a list of infrastructure requirements. 

Your objective is to complete the migration by following these steps:

1. **Transcribe the Voicemail:** 
   The previous architect left an audio message at `/app/voicemail.wav`. Use any available command-line transcription tools (like Python speech recognition libraries or whisper, which you may need to install) to decode the message. The message contains a secret project "codename" required for the Git hook.

2. **Rewrite the Legacy Parser in Rust:**
   The legacy system uses a closed-source C binary located at `/app/legacy_ticket_extractor` to parse commit messages. We are deprecating it. 
   Write a Rust program that is **strictly bit-exact equivalent** to this legacy binary. The binary reads UTF-8 text from standard input (stdin) and prints a specific transformed output to standard output (stdout). You must deduce its behavior by experimenting with it. 
   Create your Rust project in `/home/user/parser_src` and compile the release binary to `/home/user/ticket_extractor`. (An automated fuzzing verifier will test your binary against the legacy oracle with thousands of random inputs).

3. **Set up the Git Server & Hook:**
   Initialize a bare Git repository at `/home/user/config_repo.git`.
   Create a `post-receive` hook for this repository. The hook should iterate through all incoming commits. For each commit, it must extract the commit message and pipe it into your new `/home/user/ticket_extractor` binary. 
   If the output from the extractor contains the secret project codename (which you recovered from the audio voicemail), the hook must append a line to `/home/user/repo_activity.log` in this exact format:
   `[YYYY-MM-DD HH:MM:SS] Codename <extracted_output> processed`

4. **Configure Log Rotation & Storage Monitoring:**
   Create a logrotate configuration file at `/home/user/repo_logrotate.conf` that rotates `/home/user/repo_activity.log` daily, retains exactly 7 days of logs, and compresses old logs.
   Create a script at `/home/user/check_storage.sh` that calculates the disk usage of `/home/user/config_repo.git` in kilobytes (using `du -sk`). If it exceeds 50000 KB (50MB), it must append "WARNING: QUOTA EXCEEDED" to `/home/user/repo_activity.log`.

5. **Schedule Tasks:**
   Install crontab entries for the current user that run:
   - The storage monitoring script (`/home/user/check_storage.sh`) every hour at the top of the hour.
   - The logrotate configuration (`logrotate /home/user/repo_logrotate.conf --state /home/user/logrotate.state`) every day at midnight.

Ensure all scripts are executable and the Rust binary is built and placed at the exact requested path.