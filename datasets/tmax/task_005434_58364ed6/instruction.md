You are a developer tasked with organizing project files coming from a legacy, undocumented logging service. 

There is a stripped binary located at `/app/log_emitter`. When executed without arguments, it runs endlessly and rapidly dumps heavily compressed and nested archive files into the directory `/home/user/dropzone/` (it creates this directory if it doesn't exist). Because the binary writes these files dynamically, there is a race condition: it may still be writing to a file while you are trying to read it.

Your objective is to write a highly optimized Python script located at `/home/user/organizer.py` that handles this workflow:
1. Spawns the `/app/log_emitter` process in the background.
2. Monitors the `/home/user/dropzone/` directory for new archive files.
3. Safely processes the files to avoid race conditions (e.g., reading a file before the binary finishes writing it).
4. Extracts the nested archives. Every file dropped by the emitter is a `.zip` file. Inside this `.zip` file is a `.tar.gz` file. Inside the `.tar.gz` file is a single text file named `event.log`.
5. Reads the contents of `event.log` and extracts the log line.
6. Appends every successfully extracted log line into a single master file at `/home/user/master_log.txt`.
7. Cleans up the processed archives from the dropzone to save disk space.

Your script must run continuously until interrupted by a `SIGINT` or `SIGTERM`, at which point it should gracefully terminate the background emitter process and exit.

Your Python code must be fast and efficient enough to process these nested archives as quickly as they are generated. The automated testing suite will run your script for exactly 15 seconds and measure the number of valid log lines successfully written to `/home/user/master_log.txt`. You must achieve a high processing throughput to pass.