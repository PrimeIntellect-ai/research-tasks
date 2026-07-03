You are a forensics analyst investigating a compromised host. We have intercepted an audio artifact from the attacker's communication channel and recovered a cache of encoded payloads extracted from web logs. Your objective is to recover the attacker's cryptographic key from the audio file and build a Python-based classifier to identify malicious Content Security Policy (CSP) bypass payloads.

**Step 1: Audio Analysis**
An intercepted voicemail from the attacker has been saved at `/app/intercept.wav`. This audio contains a dictated, custom-encoded sequence (spoken phonetically). You must use standard command-line tools or available Python libraries (like `whisper` if installed, or any transcription/audio analysis method) to recover the spoken string. This string contains the blueprint for how the attacker encodes their malicious payloads.

**Step 2: Payload Classifier Construction**
The attacker has been sneaking malicious exfiltration scripts past our network defenses by using complex payload encoding and exploiting CSP configurations. We have extracted a dataset of payloads.
You must create a Python script at `/home/user/payload_detector.py` that analyzes an input directory of payload files. 

Your script must:
1. Accept exactly one command-line argument: the path to a directory containing text files.
   Example invocation: `python3 /home/user/payload_detector.py /path/to/corpus`
2. Read each file in the directory.
3. Decode the payload using the method deduced from the audio artifact in Step 1.
4. Perform cryptanalysis/inspection to determine if the payload is a malicious CSP bypass (e.g., attempts to inject `unsafe-inline`, unauthorized data exfiltration URIs, or malicious nonce reuse).
5. Output a JSON report to `/home/user/report.json` mapping each filename to either `"clean"` or `"evil"`.
   Example format:
   ```json
   {
     "payload_01.txt": "evil",
     "payload_02.txt": "clean"
   }
   ```

**Evaluation**
Your script will be tested against two hidden corpora: one containing strictly malicious payloads and another containing strictly benign payloads. Your script must correctly classify the payloads and write the results to `/home/user/report.json`.