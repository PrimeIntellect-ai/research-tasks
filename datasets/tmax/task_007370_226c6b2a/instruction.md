You are a backup operator automating the testing of network-based payload restores. You need to create a C++ payload verification service and a bash script to automate its testing, ensuring disk space is monitored and processes are properly managed.

Complete the following steps:

1. **Write a C++ Verifier**
Create a C++ program at `/home/user/verifier.cpp`.
- The program must listen on TCP port `9090` on `127.0.0.1`.
- It should accept a single incoming connection and read all incoming data until the connection is closed (EOF).
- After the connection closes, it must count the total number of bytes received.
- If exactly 1024 bytes were received, it must write the exact string `RESTORE VERIFIED: 1024 BYTES` followed by a newline to a log file located at `/home/user/restore_log.txt`.
- If any other number of bytes is received, it must write `RESTORE FAILED: X BYTES` (where X is the actual byte count) to the same log file.
- The program should exit cleanly after writing to the log file.

2. **Write an Automation Script**
Create a bash script at `/home/user/test_restore.sh`. The script must perform the following tasks sequentially:
- Execute `df -k /home/user` and save the output to `/home/user/disk_check.txt` to log the storage state before the test.
- Compile `/home/user/verifier.cpp` into an executable named `/home/user/verifier` using `g++`. Abort the script if compilation fails.
- Create a directory at `/home/user/restores` (if it doesn't already exist).
- Start the compiled `/home/user/verifier` process in the background.
- Give the verifier 1 second to bind to the port (e.g., using `sleep`).
- Use `dd` to generate exactly 1024 bytes of random data from `/dev/urandom` and save it to `/home/user/restores/payload.bin`.
- Use `nc` (netcat) to send the contents of `/home/user/restores/payload.bin` to `127.0.0.1` on port `9090`.
- Wait for the background verifier process to complete.

Make sure your bash script has executable permissions (`chmod +x /home/user/test_restore.sh`) and robust error handling. Do not execute the bash script; just leave it ready for the automated test suite to run.