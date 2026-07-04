You are a security researcher analyzing a suspicious data processing pipeline used by a newly discovered malware variant. You have intercepted a screen recording from the threat actor's machine, a broken proprietary decoder program, and a set of encoded payload blobs. 

Your objective is to fix the decoder, extract the secret key from the video, and write a Bash classification script to correctly identify malicious payloads.

**Step 1: Video Analysis**
You have been provided with `/app/evidence.mp4`. The threat actor accidentally flashed a QR code on the screen for a fraction of a second during this recording. 
- Use `ffmpeg` and `zbarimg` (or similar tools) to extract frames and locate the QR code.
- The QR code contains a plain text string in the format `KEY=<hex_value>`. You will need this key for the decoder.

**Step 2: Fix the Decoder**
In `/home/user/decoder_src/`, you will find the source code (`decoder.c`) and a `Makefile` for the malware's custom decryption routine.
- The program currently fails to compile due to a missing library linker flag. 
- Once compiled, running the binary (`./decoder`) crashes due to a boundary condition (an off-by-one error) in the decryption loop. Find and fix the source code.
- Furthermore, the binary enforces an environment check. It will instantly exit with an environment configuration error unless a specific environment variable, which you must reverse-engineer from the C code or binary, is correctly set.

**Step 3: Build the Detector**
The intercepted payloads are stored in two directories:
- `/app/corpora/clean/` (Benign data blobs)
- `/app/corpora/evil/` (Malicious data blobs)

Write a Bash script at `/home/user/detector.sh` that takes exactly one argument (the absolute path to a payload file).
Your script must:
1. Set the correct environment variables required by the decoder.
2. Execute the compiled `./decoder` binary, passing the payload file and the secret key (extracted from the video) as arguments (e.g., `./decoder <file> <key>`).
3. Parse the output. Malicious payloads, once decoded, will contain the exact string `C2_CONNECT_INIT`. Clean payloads will not.
4. Exit with status `1` (reject) if the payload is malicious, and status `0` (accept) if the payload is clean.

You must achieve 100% accuracy on both the clean and evil corpora. Standard tools like `ffmpeg`, `zbarimg`, `gcc`, and `make` are available in your environment.