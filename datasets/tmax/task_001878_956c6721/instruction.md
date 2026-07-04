You are an incident response security engineer. We have detected a breach in our firmware update infrastructure. An attacker generated a rogue TLS certificate and backdoored several ELF update binaries. 

Your task consists of three parts:

1. **Video Analysis**: 
   We captured a screen recording of the attacker's terminal session during the breach. It is located at `/app/incident_record.mp4`. In the video, the attacker runs an OpenSSL command to generate a rogue certificate. You must analyze the video frames to find the rogue Subject Common Name (CN) specified in the `-subj` parameter. Save this CN exactly as it appears (just the CN value, e.g., `evil-domain.local`) into `/home/user/rogue_cn.txt`.

2. **Adversarial Corpus (ELF Intrusion Detection)**:
   The attacker modified various ELF binaries. To eradicate the threat, you must write a Python script at `/home/user/detector.py` that analyzes an ELF binary and classifies it.
   Your script must take a single file path as a command-line argument.
   It must print exactly `EVIL` or `CLEAN` to standard output.
   
   A file is considered `EVIL` if it meets *either* of the following pattern-matching criteria:
   - The `.rodata` section of the ELF contains the rogue CN (the one you found in the video) encoded as ASCII.
   - The ELF binary contains a non-standard section named `.mal_tls`.
   
   If neither condition is met, it is `CLEAN`.
   You can use standard Python libraries or `pyelftools` (you may install it via pip).

3. **Credential Rotation**:
   Generate a new legitimate self-signed TLS certificate to rotate out the old ones.
   Create an RSA 2048-bit private key at `/home/user/new_key.pem` and a corresponding X.509 certificate at `/home/user/new_cert.pem`. The certificate must be valid for exactly 365 days and have the Subject Common Name `legit-update.local`.

Ensure your `/home/user/detector.py` script is robust, as we will test it against a hidden evaluation corpus of clean and evil binaries to ensure 100% accuracy.