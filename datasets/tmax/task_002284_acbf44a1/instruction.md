You are acting as a forensics analyst investigating a compromised host. We have secured a snapshot of the threat actor's staging directory located at `/home/user/evidence/`. 

The attacker attempted to hide their tracks by disguising their compiled backdoor as a benign, non-executable file. 

Your objective:
1. Examine the files in `/home/user/evidence/` and identify the hidden ELF binary. The attacker removed the executable permissions to make it look like a standard data file.
2. Analyze the binary format of this hidden ELF file. The attacker hardcoded an exfiltration key inside a custom ELF section named `.key_material`.
3. Extract the exact ASCII string stored within the `.key_material` section.
4. Save the extracted string to a file named `/home/user/recovered_key.txt`. The file should contain only the recovered key and nothing else (no section headers, offsets, or extra whitespace).

Use standard Linux command-line tools (such as those from `binutils` or `coreutils`) to accomplish this task.