You are acting as a security auditor investigating a compromised Linux system. The incident response team has provided you with a video file, `/app/audit_evidence.mp4`, which appears to be a standard screen recording of the incident. However, network logs suggest the attacker used steganography/binary-appending to exfiltrate a malicious ELF binary and configuration data within this video file.

Your objective is to complete the following phases using strictly Bash and standard Linux command-line tools:

**Phase 1: Binary Carving and ELF Analysis**
The attacker appended a raw ELF executable to the end of `/app/audit_evidence.mp4`.
1. Analyze the binary format of the MP4 file and carve out the appended ELF binary. Save it exactly to `/home/user/malware.elf`.
2. Reverse engineer / disassemble `/home/user/malware.elf` (using standard tools like `readelf`, `objdump`, or `strings`). The binary contains a hardcoded list of privilege escalation audit rules that the attacker used to score vulnerable files on the system. 
3. Identify the scoring weights assigned to the following file states: 
   - Has SUID bit set
   - Is World-Writable
   - Contains a hardcoded SSH private key (identified by the string `BEGIN OPENSSH PRIVATE KEY`)

**Phase 2: Privilege Escalation Auditing**
Using the rules and weights you extracted from the binary, write a Bash script at `/home/user/audit_system.sh` that automatically scores files.
1. The script must scan all files within `/app/system_root/`.
2. For each file, calculate its vulnerability score based on the extracted weights (starting at 0, adding the respective weight if the condition is met).
3. The script must output the results to `/home/user/audit_scores.csv` in the exact format: `filepath,score` (e.g., `/app/system_root/etc/passwd,50`).

**Phase 3: Video Frame Extraction (Bonus/Validation)**
The video itself flashes a specific sequence of red frames (RGB: 255,0,0) that correspond to the exact timestamps when the attacker triggered an exploit. Use `ffmpeg` to analyze the video and extract the timestamps (in seconds) of any completely red frame. Append these timestamps, one per line, to `/home/user/red_frames.txt`.

Ensure your scoring is perfectly accurate. An automated metric verifier will compare your generated `audit_scores.csv` against the ground truth to calculate the Mean Absolute Error (MAE) of your vulnerability scores. 

You must meet an MAE of 0.0 (perfect accuracy) on the scoring to pass.