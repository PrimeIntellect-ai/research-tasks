You are a security researcher analyzing a suspicious binary found on a compromised Linux system. The binary is located at `/home/user/vuln_bin` and appears to process batch command files. We know it occasionally crashes with a Segmentation Fault when processing large batches of captured traffic, but we don't know exactly why.

Your task is to debug this binary, isolate the vulnerability, and create a reliable regression test.

Here is what you need to do:

1. **Delta Debugging**: You have been provided with a large capture of commands in `/home/user/capture.txt` (one command per line). Most of these commands are benign. You must write a script to perform delta debugging (test minimization) to find the absolute minimum subset of lines from `capture.txt` that still reliably causes `/home/user/vuln_bin` to crash with a segfault. Keep the relative order of the lines intact.
   Save this minimal set of commands to `/home/user/minimal.txt`.

2. **Crash Analysis**: Run the binary with your minimal input and use `gdb` (or another debugging tool) to analyze the crash. Identify the exact C function name where the segmentation fault occurs (the function attempting the invalid memory access).
   Write ONLY the exact function name to `/home/user/crash_func.txt`.

3. **Regression Test Construction**: Write a Python script at `/home/user/poc.py` that acts as a regression test. 
   - The script should execute `/home/user/vuln_bin` and pass it your minimal payload (either by creating a temporary file or using `minimal.txt`).
   - The script must exit with status code `0` if the binary crashes with a segmentation fault (indicating the vulnerability was successfully triggered).
   - The script must exit with status code `1` if the binary exits normally or with a non-segfault error.

**Execution Constraints:**
- The binary is executed as: `/home/user/vuln_bin <input_file>`
- You may use any standard Linux tools available (Python, gdb, bash, etc.).
- Ensure your `poc.py` is executable (`chmod +x /home/user/poc.py`).