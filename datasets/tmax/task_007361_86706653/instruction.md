You are acting as a storage administrator to manage a buggy log rotation system. We have a script that writes JSON log files and then zips them. Unfortunately, the zipping process sometimes races with the disk writer, producing corrupted `.zip` archives.

Your task is to write a C program that acts as a monitor, watching the incoming directory in real-time, verifying the integrity of the zipped logs, and extracting metadata from the original JSON files when a zip is found to be corrupt.

Here are the specific requirements:
1. Create a C program at `/home/user/monitor.c` and compile it to `/home/user/monitor`.
2. The program must use Linux `inotify` to watch the directory `/home/user/incoming` for newly finished `.zip` files (hint: watch for `IN_CLOSE_WRITE` events).
3. When a `.zip` file is closed, the program must verify its archive integrity. You may use external commands like `unzip -t` via `system()` or `popen()` to perform this check.
4. If the `.zip` file is corrupted (integrity check fails), your program must open the corresponding `.json` file (e.g., if `log_3.zip` is corrupt, open `log_3.json`).
5. Parse the JSON file to extract the `id` (integer) and `status` (string). The JSON format will always be strictly flat, like: `{"id": 3, "status": "ERROR", "data": "..."}`. You can use manual string parsing.
6. Append the extracted data to `/home/user/bad_logs.csv` in the format: `id,status` (e.g., `3,ERROR`) with a newline.
7. The program should cleanly exit after it successfully processes an event for `log_10.zip` (valid or invalid).

To test your program:
1. Compile your code: `gcc /home/user/monitor.c -o /home/user/monitor`
2. Start your monitor program in the background: `/home/user/monitor &`
3. Run the log generator script (which we have already prepared): `/home/user/generate_logs.sh`
4. Wait for your monitor to exit.

Please implement the solution, run the generator, and ensure `/home/user/bad_logs.csv` contains the correct entries for all corrupted archives.