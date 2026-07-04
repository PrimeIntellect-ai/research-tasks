You are a security researcher analyzing a suspicious Python script found on a compromised Linux server. The script is located at `/home/user/suspicious.py`. 

Incident response indicates that when this script is executed with a specific large configuration file, currently stored at `/home/user/input.txt`, it drops a hidden payload somewhere on the filesystem. However, `input.txt` contains hundreds of lines of configuration data, and manual inspection of the obfuscated Python script has been difficult.

Your objectives are to trace the script's execution and isolate the trigger. You must complete the following tasks:

1. **System Call Tracing**: Use system call tracing tools on `suspicious.py` (running with `input.txt` as its argument) to identify the absolute path of the hidden file being written to the filesystem. 
   - Write the absolute path of this dropped file to `/home/user/target_file.log` (ensure it contains nothing else, no trailing newlines if possible, just the path).

2. **Intermediate State Tracing**: Analyze the script's intermediate state during execution to extract the exact decoded payload (a string) that gets written to the hidden file. 
   - Save this exact string to `/home/user/payload.log`.

3. **Delta Debugging / Minimization**: The `input.txt` file is large, but only one specific line inside it triggers the malicious behavior. Use delta debugging or test minimization techniques to isolate this exact line.
   - Create a new file at `/home/user/minimized_input.txt` that contains *only* the single line from `input.txt` necessary to trigger the payload drop.

Constraints:
- Do not modify the original `suspicious.py` or `input.txt` files.
- You have access to standard Linux utilities (like `strace`) and Python 3.
- Execute the script via: `python3 /home/user/suspicious.py /home/user/input.txt`