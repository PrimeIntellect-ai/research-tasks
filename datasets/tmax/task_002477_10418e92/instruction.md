You have been hired as a Security Auditor to investigate a legacy secure voice logging system. During an initial network sweep, your team intercepted an encrypted audio file located at `/app/evidence.enc` and retrieved the system's decryption daemon, located at `/app/vault_decrypt`.

Your objective is to successfully decrypt the audio file and transcribe the hidden spoken message into `/home/user/transcript.txt`. 

To achieve this, you must navigate several layers of the system's security controls:

1. **Reverse Engineering & Access Control:** 
   The `/app/vault_decrypt` binary is compiled and undocumented. You must analyze the binary to determine its internal access control checks. It expects a specific directory structure, exact file permissions, and process isolation conditions (e.g., running under specific constraints or user IDs) before it will execute.

2. **Cryptographic Authentication:**
   The daemon requires a client TLS/SSL certificate and private key to authenticate the decryption request. Through your disassembly/analysis of the binary, you will find the required filesystem paths where it expects these cryptographic materials, the strict file permissions required for the private key, and the specific X.509 Subject attributes (e.g., Organization or Common Name) hardcoded into the binary's validation logic. You must use shell tools (like `openssl`) to generate a self-signed certificate that satisfies these checks.

3. **Execution & Sandboxing:**
   Once the environment, certificates, and permissions are correctly staged, execute the binary. It takes the input encrypted file and an output path as arguments (e.g., `/app/vault_decrypt /app/evidence.enc /tmp/decrypted.wav`). If your setup is correct, it will decrypt the audio.

4. **Transcription:**
   Once decrypted, use the pre-installed transcription tool (a mock `whisper-cli` or `ffmpeg` pipeline available in the environment) to transcribe the English audio. Save the plain text transcription to exactly `/home/user/transcript.txt`.

**Constraints & Deliverables:**
- The automated verification system will read `/home/user/transcript.txt` and compare it against the hidden ground truth using a string similarity metric.
- Your solution should utilize standard bash built-ins, coreutils, and any necessary scripting to glue the components together.
- Do not attempt to brute-force the encryption; the binary contains the decryption logic natively once its environmental and cryptographic authentication checks are satisfied.