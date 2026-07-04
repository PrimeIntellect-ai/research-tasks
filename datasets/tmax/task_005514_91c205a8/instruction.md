You have inherited an unfamiliar, undocumented legacy system. A background worker script named `legacy_worker.sh` is currently running on the system. This script is supposed to load and process a critical system token, but it appears to be hung and is not producing any output.

Through preliminary investigation, we know the script's behavior:
1. It generates or receives a critical token.
2. It writes this token to a temporary file.
3. It opens the temporary file for reading.
4. It immediately deletes (unlinks) the temporary file from the filesystem for security purposes.
5. It then proceeds to its processing loop, where it is currently stuck.

Your task is to inspect the running system, recover the critical token from the hanging process without killing it, and save the recovered token into a new file located at `/home/user/recovered_token.txt`. 

Requirements:
- The file `/home/user/recovered_token.txt` must contain exactly the token string and nothing else (a trailing newline is acceptable).
- Do not kill or restart the `legacy_worker.sh` process.
- Rely on system debugging techniques (such as inspecting process states, file descriptors, or memory) to extract the data.