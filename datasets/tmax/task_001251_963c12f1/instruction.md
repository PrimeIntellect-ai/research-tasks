You are a forensics analyst investigating a compromised Linux host. An attacker exploited a path traversal vulnerability in a file upload handler to drop a malicious Python payload outside the designated upload directory.

Your task is to locate the anomalous payload, verify the integrity of the filesystem, and safely analyze the malware's behavior.

1. **Integrity Verification**: 
   A list of expected, legitimate file SHA-256 hashes is located at `/home/user/manifest.txt`. 
   Search the directories `/home/user/uploads/` and `/home/user/system_cache/` to find the single file whose hash is NOT present in the manifest. This is the malicious payload.

2. **Process Isolation & Network Policy**:
   You must execute this malicious Python script to analyze its output, but you must do so securely to prevent it from phoning home or modifying the system.
   Write a Python script at `/home/user/analyze.py` that uses the `subprocess` module to execute the malicious payload using `bwrap` (Bubblewrap) with the following strict sandboxing rules:
   - Completely disable network access (`--unshare-net`)
   - Mount the root filesystem as read-only (`--ro-bind / /`)
   - Mount `/proc` (`--proc /proc`)
   - Mount `/dev` (`--dev /dev`)
   
3. **Evidence Collection**:
   Your `/home/user/analyze.py` script should capture the standard output of the sandboxed malicious payload and write it exactly to `/home/user/malware_output.txt`.

Ensure your `analyze.py` script is fully functional and successfully writes the output to the destination file.