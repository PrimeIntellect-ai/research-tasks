**Deliverable:** A Python script at `/home/user/payload_generator.py` that accepts a single string argument and outputs a perfectly formatted port-knocking sequence payload to standard output. 

**Context & Setup:**
As a penetration tester, you have intercepted a video recording of an administrator performing a proprietary port-knocking sequence to unlock a hidden service. The video is located at `/app/intercepted_knock.mp4`. 

Additionally, you have obtained a compiled, stripped Linux binary (`/app/oracle_validator`) that the server uses to validate incoming payloads. Your objective is to reverse-engineer the encoding and hashing logic used in this proprietary sequence and write a Python script that exactly replicates the binary's output for any given input string.

**Requirements:**
1. Analyze `/app/intercepted_knock.mp4`. The video contains frames displaying raw text inputs and their corresponding base64-encoded, hashed port-knock payloads. Use `ffmpeg` to extract frames and analyze the transformation.
2. The transformation involves a custom combination of payload encoding (Base64 variants) and cryptographic hashing (SHA256 checksum generation).
3. The server binary `/app/oracle_validator` takes a single command-line argument (the raw string) and prints the final port-knock payload to `stdout`.
4. Your script `/home/user/payload_generator.py` must be written in Python. It must take exactly one argument (`sys.argv[1]`) and print the exact same string as the oracle.
5. Your script must be standalone and deterministic.
6. Make sure your script is executable (`chmod +x /home/user/payload_generator.py`).