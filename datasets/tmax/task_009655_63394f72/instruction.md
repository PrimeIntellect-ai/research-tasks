You are acting as a red-team operator crafting an evasion payload to test a web application's defenses. The target application requires a Proof-of-Work (PoW) hash collision to accept uploads, runs a naive content scanner, and is suspected to be vulnerable to path traversal.

Your objective is to analyze the application's source code, craft a specific bypassing payload, and compute the correct path traversal sequence. 

Step 1: Vulnerability Analysis
Explore the application handler source codes located in `/home/user/app/handlers/`. There are several Python scripts in this directory. Only one of these scripts contains a direct, unparameterized SQL injection vulnerability (string formatting/concatenation directly into an SQL query). 
Identify this vulnerable file. The name of this file (excluding the `.py` extension) will be used as the `MODULE_NAME` in the next step.

Step 2: Payload Crafting & Brute-Force
The application filters out files unless they pass a Proof-of-Work check. You must craft a payload string that strictly follows this format:
`[MODULE_NAME]:<svg onload=alert(1)>:[NONCE]`

Where:
- `[MODULE_NAME]` is the name of the vulnerable file you identified (without `.py`).
- `<svg onload=alert(1)>` is the exact XSS payload string provided here.
- `[NONCE]` is a positive integer (e.g., 1, 2, 3...).

You must write a Python script to brute-force the `[NONCE]` value starting from 1. You are looking for the smallest positive integer nonce such that the MD5 hash (in lowercase hexadecimal) of the *entire* payload string begins with exactly five zeros (`00000`).

Once you find the correct nonce, write the complete, successful payload string (e.g., `module:<svg onload=alert(1)>:12345`) to the file `/home/user/final_payload.txt`. Do not include any trailing newlines in this file.

Step 3: Path Traversal
The web application extracts and saves uploaded files into the directory `/home/user/app/public/uploads/`. 
You want to exploit a path traversal vulnerability in the upload handler to overwrite a configuration file located exactly at `/home/user/secret_config.json`.
Determine the minimal relative file path (using `../`) that, when appended to the application's upload directory, resolves to the target configuration file. 
Write this exact relative path string to `/home/user/traversal_path.txt`. Do not include trailing newlines.