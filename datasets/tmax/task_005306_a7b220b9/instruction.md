You are acting as a site administrator for a legacy multi-tenant environment. The previous administrator left abruptly, leaving behind a partially migrated system for assigning dedicated application ports to user accounts.

Your objective is to complete the migration by reverse-engineering the port mapping algorithm, implementing a robust process supervisor, and writing a staged deployment script.

**Part 1: The Port Mapping Algorithm**
The previous admin left an audio voicemail at `/app/sysadmin_memo.wav`. You must transcribe this audio to discover the "secret salt" used in the new port assignment algorithm.
The algorithm to determine a user's port is:
1. Calculate the sum of the ASCII decimal values of all characters in the provided username.
2. Add the secret salt (mentioned in the audio).
3. Modulo the result by 1000.
4. Add 8000 to get the final port number.

Write a Bash script at `/home/user/port_mapper.sh` that takes exactly one argument (the username, which will be a lowercase alphanumeric string of 4-12 characters) and prints ONLY the calculated port number to standard output. 

**Part 2: Process Supervision**
Write a Bash script at `/home/user/supervise.sh` that acts as a process supervisor. It should take one argument (a port number). 
The script must:
1. Launch `python3 -m http.server <port>` in the foreground.
2. If the python server crashes or is killed, the supervisor must immediately restart it.
3. It must continue this loop indefinitely.

**Part 3: Staged Deployment & Connectivity Diagnostics**
Write a deployment script at `/home/user/deploy.sh` that takes a username as an argument.
The script must:
1. Use `/home/user/port_mapper.sh` to determine the user's port.
2. Launch `/home/user/supervise.sh <port>` in the background (staged deployment).
3. Continuously poll the port using `curl`, `nc`, or `/dev/tcp` with a 1-second delay between attempts (connectivity diagnostic).
4. Once the port is successfully responding, append the exact string `Deployment successful for user: <username> on port: <port>` to `/home/user/deploy.log` and exit successfully.

Ensure all scripts are executable (`chmod +x`). Do not use root privileges.