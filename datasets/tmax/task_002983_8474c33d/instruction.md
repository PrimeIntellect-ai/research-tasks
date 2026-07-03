You are a compliance analyst tasked with generating an automated audit trail system for analyzing web application logs. The system administrators have provided you with an encrypted archive of historical payloads, but the password was left on a secure voicemail system.

**Stage 1: Environment & Password Recovery**
There is an audio recording located at `/app/voicemail.wav`. The recording contains standard DTMF (Dual-Tone Multi-Frequency) tones that represent a 6-digit PIN.
1. Analyze the audio file to decode the 6-digit PIN.
2. Use this PIN to decrypt and extract the archive `/app/audit_logs.zip` into `/app/corpus/`.

**Stage 2: Payload Decoder & Vulnerability Scanner**
The extracted archive contains two directories: `/app/corpus/clean/` and `/app/corpus/evil/`. These directories contain files representing isolated HTTP parameter payloads that have been captured by our firewall. The payloads are URL-encoded.

Your task is to develop a custom vulnerability scanner in C++ that categorizes these payloads to generate compliance alerts.
1. Create a C++ source file at `/home/user/sanitizer.cpp` and compile it to `/home/user/sanitizer`.
2. The binary must accept exactly one argument: the absolute path to a payload file.
    Example invocation: `/home/user/sanitizer /app/corpus/evil/payload_01.txt`
3. The program must read the file contents and URL-decode the payload.
4. After decoding, the program must scan the payload for signs of path traversal (e.g., `../`, `..\`) or command injection shell metacharacters (e.g., `;`, `|`, `` ` ``, `$()`).
5. **Output Requirements:**
    * If the payload is determined to be malicious, the program must print exactly `EVIL` to standard output and terminate with exit code `1`.
    * If the payload is benign, the program must print exactly `CLEAN` to standard output and terminate with exit code `0`.

**Acceptance Criteria:**
We will run an automated test suite against your compiled `/home/user/sanitizer` binary. It must correctly reject 100% of the payloads in the `evil` corpus and correctly accept 100% of the payloads in the `clean` corpus. Ensure your C++ implementation is robust and handles standard URL encoding correctly.