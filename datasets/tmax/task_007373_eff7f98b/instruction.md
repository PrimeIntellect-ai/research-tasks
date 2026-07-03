You are an expert security researcher. You have intercepted a suspicious binary located at `/home/user/bin/suspicious_parser` on your system. 

Initial analysis suggests this binary parses custom configuration files, but it currently refuses to run. 

Your objectives are to fix the environment so the binary can run, discover a critical memory corruption vulnerability by writing a fuzzer, and analyze the crash traceback.

**Phase 1: Environment Repair**
When you attempt to run `/home/user/bin/suspicious_parser`, it fails to execute or immediately aborts due to a misconfigured environment. There is a missing dynamic library and a missing environment variable. 
Fix the environment configuration for the current shell so that running the binary without arguments successfully prints its usage instructions.

**Phase 2: Fuzz Testing**
The binary takes a single file path as an argument. 
Reverse engineering (or reading its initial output) indicates that valid configuration files must start with the exact magic header:
`SECURE_CONF_v1`
followed by a newline, and then a line starting with:
`NAME:`

Write a fuzzer in the language of your choice to generate variations of this file format. Your goal is to find an input that causes the binary to crash with a **Segmentation fault (core dumped)**. 
Once your fuzzer finds the crashing input, save the exact contents of the payload that caused the crash to `/home/user/crash_payload.txt`.

**Phase 3: Traceback Analysis**
Using `gdb` or any other debugging tool, analyze the crash caused by your payload. Identify the exact name of the C function inside the binary where the buffer overflow / segmentation fault occurs.
Write the exact name of this vulnerable function to `/home/user/vulnerable_function.txt` (just the function name, no other text).

**Deliverables:**
1. A fixed environment allowing the execution of `/home/user/bin/suspicious_parser`.
2. A file `/home/user/crash_payload.txt` containing the exact input that causes the segmentation fault.
3. A file `/home/user/vulnerable_function.txt` containing the name of the function where the crash occurs.