You are acting as a backup operator. We are building an automated pipeline to test restored VM backups and sanitize their extracted configuration files before re-integration.

You need to complete a multi-stage workflow:

1. **Audio Rules Extraction**
   Listen to the voicemail left by the senior security administrator located at `/app/voicemail_backup.wav`. This audio contains spoken instructions detailing the precise keywords that indicate a configuration file is compromised ("evil") and the required keywords for a configuration file to be considered valid ("clean"). You will likely need to use a tool like `whisper-cli` or `ffmpeg` to extract or transcribe the audio.

2. **C++ Sanitizer Implementation**
   Write a C++ program at `/home/user/sanitizer.cpp` and compile it to `/home/user/sanitizer`.
   - The executable must take exactly one command-line argument: the absolute path to a file to analyze.
   - It must read the file and determine if it is "clean" or "evil" based strictly on the rules you transcribed from the voicemail.
   - It must exit with code `0` if the file is clean, and exit with code `1` if the file is evil.
   
   Test your program against the provided corpora located in `/app/corpus/clean/` and `/app/corpus/evil/`. Your compiled `/home/user/sanitizer` must successfully exit with `0` for all files in the clean directory and `1` for all files in the evil directory.

3. **VM Restore Supervisor**
   Write a bash script at `/home/user/vm_supervisor.sh` that simulates booting a restored disk.
   - The script must run the following command: `qemu-system-x86_64 -m 256 -drive file=/app/dummy_disk.qcow2,format=qcow2 -nographic -daemonize -pidfile /home/user/qemu.pid`
   - Make sure the script is executable.

4. **Process Supervision & Scheduling**
   Create a user-level systemd service named `vm-restore.service` that executes your `/home/user/vm_supervisor.sh` script. 
   - Then, create a systemd timer named `vm-restore.timer` that is configured to start this service every 15 minutes.
   - Enable and start the timer for the current user.

Ensure your C++ sanitizer is perfectly accurate. The automated verification will test your compiled `/home/user/sanitizer` against a hidden set of clean and evil files generated using the exact same rules described in the audio.