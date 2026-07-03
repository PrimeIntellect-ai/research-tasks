I am a performance engineer profiling our C++ log data processing tool. During a recent test, the application unexpectedly crashed. I was analyzing the specific input file (`/tmp/crash_data.txt`) that caused the crash, but I accidentally deleted it! 

Fortunately, I had started a background process (`tail -f /tmp/crash_data.txt > /dev/null &`) to monitor it right before I accidentally ran `rm`. Because the `tail` process is still running, the file's data should still be recoverable from memory/file descriptors.

Your task is to:
1. **Recover the deleted file**: Extract the deleted file's contents using the running `tail` process and save it exactly as `/home/user/recovered.txt`.
2. **Create a Minimal Reproducible Example (MRE)**: Identify the *single line* within the recovered data that causes the C++ tool to crash. Save this single line to `/home/user/mre.txt`.
3. **Fix the Application**: The source code for the tool is located at `/home/user/process_logs.cpp`. Analyze the code and the MRE to determine why it crashes (it throws an uncaught exception). Fix the bug in `/home/user/process_logs.cpp` so that it safely ignores or bounds-checks the malformed line without crashing.
4. **Compile the Fix**: Compile your fixed code using `g++ -O2 /home/user/process_logs.cpp -o /home/user/process_logs_fixed`.

Verify that running `/home/user/process_logs_fixed < /home/user/mre.txt` exits cleanly with a 0 exit code and does not abort.