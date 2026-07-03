You are a DevOps engineer tasked with debugging a fragile log ingestion pipeline. The pipeline uses a C program `log_ingestor` which links against a legacy, black-box shared library called `libfilter.so` (for which we no longer have the source code). Recently, the ingestor started crashing with a segmentation fault when processing the daily logs in `/home/user/logs/`.

Your tasks are:
1. **Identify the Crash:** Run the ingestor against the log files in `/home/user/logs/` to determine which specific log file and line is causing the segmentation fault.
2. **Reverse Engineer & Fuzz:** Analyze `libfilter.so` (using tools like `gdb`, `objdump`, or `ltrace`) and write a Python fuzzer (`/home/user/fuzzer.py`) to determine the exact crash condition. The library function `int filter_log(const char* log_line)` crashes when a specific field in the log line exceeds a certain length. 
3. **Handle Corrupted Input:** Modify `/home/user/log_ingestor.c` to gracefully handle these corrupted log entries. You must add sanitization logic to truncate the oversized field to its maximum safe length before passing it to `filter_log`. 
4. **Assertion-Based Validation:** In `/home/user/log_ingestor.c`, add an `assert()` statement right before the `filter_log` call to validate that the extracted field strictly adheres to the safe length limit you discovered, preventing any future overflow in the legacy library.
5. **Rebuild and Test:** Recompile `log_ingestor` (linking against `/home/user/libfilter.so`) and ensure it successfully processes all logs in `/home/user/logs/` without crashing.
6. **Report:** Create a file at `/home/user/solution.txt` containing exactly two lines:
   - Line 1: The filename of the log file that originally caused the crash (e.g., `app_03.log`).
   - Line 2: The maximum safe length (an integer) of the payload for the vulnerable field before it causes a crash.

Requirements:
- Do not modify the `Makefile` or the legacy library.
- Use `gcc` to compile your modified `log_ingestor.c`. Run: `gcc -o /home/user/log_ingestor /home/user/log_ingestor.c -L/home/user -lfilter -Wl,-rpath=/home/user`
- Standard system tools (Python 3, GDB, objdump, GCC) are available.