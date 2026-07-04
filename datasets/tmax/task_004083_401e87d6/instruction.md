You are acting as a security auditor for a secure kiosk system. You have two primary objectives to complete your audit.

**Objective 1: Video Audit Log Analysis**
The system records physical access attempts via an LED status indicator, saved as an MP4 video at `/app/audit_log.mp4`.
1. Use `ffmpeg` to extract the frames of this video.
2. The video consists of solid colored frames. Analyze the extracted frames to count the exact number of "Access Denied" events. An "Access Denied" event is represented by a frame that is completely solid red (Hex: `#FF0000`, RGB: `255, 0, 0`).
3. Write the integer count of red frames to `/home/user/red_frame_count.txt`.

**Objective 2: Policy File Validator (C++)**
The kiosk uses policy files to configure its permissions, content security policy, and certificate trust chains. You must write a C++ program to validate these files.
Create your source code at `/home/user/policy_validator.cpp` and compile it to `/home/user/validator`.

The program must take a single file path as a command-line argument:
`/home/user/validator <path_to_policy_file>`

It must exit with code `0` if the file is perfectly valid, and exit with a non-zero code (e.g., `1`) if it violates ANY of the security rules below.

**Security Rules for a Valid Policy File:**
1. **File Integrity:** The first line of the file must exactly match the format `HASH: <64-character SHA256 hex string>`. The SHA256 string must be the exact SHA256 hash of the *entire remainder of the file* (starting immediately from the character after the newline of the first line, to the EOF).
2. **Content Security Policy Enforcement:** The file must contain a line starting with `CSP: `. The rest of this line contains the CSP directives. To be valid, the CSP string MUST NOT contain the substrings `unsafe-inline` or `unsafe-eval`.
3. **Certificate Chain Validation:** The file must contain a line starting with `CERT_CHAIN: ` followed by a comma-separated list of certificate names (e.g., `CERT_CHAIN: RootCA,IntermediateCA,LeafCA`). A valid chain MUST start exactly with `RootCA`, MUST end exactly with `LeafCA`, and MUST NOT contain the string `RevokedCA` anywhere in the chain.

**Validation against Corpora:**
We have provided two sets of test policies:
- `/app/corpus/clean/`: Contains strictly valid policy files. Your program must exit `0` for all of them.
- `/app/corpus/evil/`: Contains policies that violate one or more of the rules (tampered hashes, unsafe CSPs, or invalid cert chains). Your program must exit non-zero for all of them.

Ensure your C++ program is robust and handles missing files or malformed formats gracefully by rejecting them (non-zero exit). You may use standard Unix tools (like `sha256sum` via `popen` or system calls, or standard C++ libraries) to implement the checks.