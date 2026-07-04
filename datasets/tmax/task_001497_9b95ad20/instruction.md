You are the on-call engineer for a critical security system. It's 3 AM, and you've just been paged because the primary intrusion detection system (IDS) went down, leaving the facility vulnerable.

You need to investigate the incident, recover the data, patch the vulnerability, and correlate it with physical evidence.

**Step 1: Database Recovery & Traceback Analysis**
The IDS uses a custom Go-based append-only Write-Ahead Log (WAL). The process crashed midway through a write, corrupting the active log file located at `/app/corrupted.wal`.
The crash traceback is saved in `/app/crash.log`.
The WAL format is binary, consisting of sequential records:
1. Magic header: `WAL1` (4 bytes: `0x57 0x41 0x4C 0x31`)
2. Payload length: Unsigned 32-bit integer, little-endian (4 bytes)
3. Payload: JSON data (length bytes)
4. Checksum: CRC32 (IEEE) of the payload data, unsigned 32-bit integer, little-endian (4 bytes)

Write a Go program at `/home/user/recover.go` that parses `/app/corrupted.wal`. It must extract all valid JSON payloads (where the CRC32 matches), gracefully skip over any corrupted byte ranges by scanning for the next `WAL1` magic header, and append each valid JSON payload on a new line to `/home/user/recovered.jsonl`.

**Step 2: Adversarial Sanitizer**
Analysis of `/app/crash.log` reveals the crash was a deliberate attack (a "poison pill" payload) that triggered a panic in the log parser.
You must create a Go-based sanitizer to prevent this in the future.
Write a program at `/home/user/sanitizer.go` that takes a single file path as a command-line argument.
- It must exit with code `0` if the payload is safe ("clean").
- It must exit with code `1` if the payload is malicious ("evil").
You are provided with examples of malicious payloads in `/app/corpus/evil/` and safe payloads in `/app/corpus/clean/`. Analyze them alongside the crash log to determine the exact vulnerability pattern. The automated system will compile your sanitizer and test it against a hidden evaluation corpus.

**Step 3: Video Artifact Correlation**
The attacker physically tampered with a camera to mask their entry. The footage from the incident is available at `/app/incident.mp4`.
Extract the frames and analyze them to find the exact contiguous frame range where the camera was blinded (defined as frames where the average pixel intensity is strictly less than 15 out of 255).
Write the start and end frame numbers (0-indexed, inclusive) to `/home/user/video_event.txt` in the format `START-END` (e.g., `45-120`).

Complete these tasks to resolve the page.