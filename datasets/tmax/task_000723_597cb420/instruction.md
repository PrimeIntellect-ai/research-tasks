You are a storage administrator responsible for managing disk space and user uploads. Recently, we've had issues with users uploading malicious archives designed to overwrite system files outside their designated extraction directories (a vulnerability known as "Zip Slip").

To secure our extraction pipeline, we need a robust path validation tool. 

Your task consists of two parts:

1. **Information Retrieval:** 
   Listen to the audio file located at `/app/policy.wav`. This file contains a recorded message from the Chief Security Officer detailing the exact security rejection code that MUST be printed when a path traversal attempt is detected. You will need to transcribe or listen to this audio file to get the exact uppercase rejection code.

2. **Path Validator Implementation:**
   Write a script at `/home/user/path_validator.py` that takes exactly two command-line arguments:
   `python3 /home/user/path_validator.py <base_dir> <untrusted_path>`
   
   The script must:
   - Normalize and compute the absolute path of `<base_dir>`.
   - Resolve the `<untrusted_path>` relative to `<base_dir>` and compute its normalized absolute path.
   - If the resolved path is strictly a descendant of the normalized `<base_dir>` (i.e., it sits safely inside the directory), print the normalized absolute path to standard output.
   - If the resolved path is equal to `<base_dir>` or escapes outside of `<base_dir>` (a Zip Slip attempt), print EXACTLY the rejection code you recovered from the audio file to standard output.
   - Do NOT print anything else to standard output.

We will verify your script against thousands of generated edge-case paths (including deeply nested `../`, symlink-like strings, and tricky absolute path injections) to ensure its behavior is bit-exact equivalent to our strict internal security oracle.