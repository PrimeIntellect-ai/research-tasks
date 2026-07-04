You are a network security engineer investigating a sophisticated malware strain. You suspect the malware is exfiltrating data by encoding payloads and passing them as command-line arguments (visible in `/proc`). 

We have intercepted a diagnostic video feed from the compromised system's network dashboard, as well as a sample of intercepted process arguments.

Your objective is to build a C++ intrusion detection tool (`/home/user/detector`) that classifies intercepted process payloads as either clean or malicious.

**Step 1: Key Recovery**
The malware operators leaked their symmetric encryption key through a steganographic channel in a dashboard visualization video located at `/app/capture.mp4`. 
- The video is exactly 256 frames long.
- The exact center pixel of the video `(width/2, height/2)` encodes a single bit per frame, ordered from frame 1 to 256. 
- If the Red channel of that pixel is > 128, the bit is `1`. Otherwise, it is `0`.
- Extract these 256 bits and pack them into a 32-byte key (byte 0 is formed by frames 1-8, where frame 1 is the most significant bit, etc.).

**Step 2: Payload Decoder & Classifier**
Write a C++ program and compile it to `/home/user/detector`. The program must take a single file path as a command-line argument:
`./detector /path/to/payload.txt`

The target file will contain a single Base64-encoded string. Your C++ program must:
1. Read the Base64 string from the file and decode it into raw bytes.
2. Decrypt the raw bytes by applying a repeating XOR cipher using the 32-byte key you recovered from the video.
3. Perform pattern matching on the decrypted plaintext. If the plaintext contains a string matching the regular expression `EXFIL-[A-Z0-9]{4}`, it is malicious.
4. Exit with status code `1` if the payload is malicious.
5. Exit with status code `0` if the payload is clean (benign).

**Validation**
You have been provided with two directories of sample payloads to test your detector:
- `/app/corpus/evil/` contains 50 malicious payloads.
- `/app/corpus/clean/` contains 50 benign payloads.

You must ensure your `/home/user/detector` binary correctly flags 100% of the evil corpus (exit code 1) and accepts 100% of the clean corpus (exit code 0). When you are confident in your binary, an automated verifier will test it against these corpora.