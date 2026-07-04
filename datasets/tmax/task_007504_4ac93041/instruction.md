You are a backup operator building a local mock CI/CD pipeline to test the reliability of a custom restore receiving daemon. 

You have been provided with the source code for a C++ daemon at `/home/user/restore_daemon.cpp`. This daemon receives backup chunks over TCP on port 8080 and writes them to `/home/user/restored_data.bin`. It is also designed to simulate a transient failure: if it receives the exact string "CRASH_TEST", it will immediately crash and exit with a non-zero status.

Your task consists of two parts:

**Part 1: Fix the C++ Daemon**
The provided `restore_daemon.cpp` has a bug: it currently binds specifically to the loopback address, but for our tests, it must bind to all available interfaces (`INADDR_ANY`). Modify the C++ code to bind to `INADDR_ANY` and ensure it compiles successfully. Compile the code using `g++` and output the binary to `/home/user/restore_daemon`.

**Part 2: Build the Pipeline Script**
Create a bash script at `/home/user/pipeline.sh` that implements the mock CI/CD test. The script must perform the following steps in order:
1. **Process Supervision**: Start `/home/user/restore_daemon` in the background. Wrap it in a bash loop that acts as a simple process supervisor: if the daemon exits with a non-zero exit code (crashes), the supervisor should automatically restart it. If it exits with code 0 (success), the supervisor should terminate.
2. **Connectivity Diagnostics**: Implement a check using standard bash tools (like `nc` or `/dev/tcp`) to poll and wait until the daemon is actively listening on port 8080.
3. **Simulate Failure**: Once the port is open, send the string `CRASH_TEST` to the daemon via the network. This will cause the daemon to crash, which should trigger your supervisor to restart it.
4. **Wait for Recovery**: Poll again and wait until the restarted daemon is listening on port 8080.
5. **Test Restore**: Send the exact contents of the dummy backup file located at `/home/user/backup_archive.tar.gz` to the daemon over the network.
6. **Verification**: Wait for the daemon to cleanly exit (which it does after successfully receiving data and closing the connection). Ensure the resulting `/home/user/restored_data.bin` matches the original `/home/user/backup_archive.tar.gz`.
7. **Reporting**: If the pipeline completes successfully and the restored file matches the original, write the exact string `PIPELINE SUCCESS` to `/home/user/pipeline_result.log`.

Make sure your script is executable and run it to perform the test. Ensure that at the end of your session, `/home/user/pipeline_result.log` contains the success message and `/home/user/restored_data.bin` is correctly restored.