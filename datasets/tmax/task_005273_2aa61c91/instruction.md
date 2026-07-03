You are acting as a network security engineer investigating a recent breach on a compromised Linux workstation. We suspect the attacker exfiltrated data by obfuscating network payloads and left a persistent backdoor. 

Your objectives are divided into three phases: Threat Intelligence Extraction, Backdoor Remediation, and Payload Decoder Implementation.

**Phase 1: Threat Intelligence Extraction**
We intercepted an image file that the attacker exfiltrated. It is located at `/app/capture.png`. We believe it contains a configuration snippet or a key used to obfuscate their command-and-control (C2) traffic. 
1. Use any available tools (like `tesseract`) to extract the text from this image.
2. Identify the numeric `DECODER_KEY` value hidden in the text.

**Phase 2: Backdoor Remediation & Hardening**
The attacker modified your SSH configuration to maintain access. 
1. Audit your `/home/user/.ssh/authorized_keys` file. You will find multiple keys. Remove the key that ends with the comment `hacker@c2-server`. Do not alter the other legitimate keys.
2. The attacker also messed up your SSH directory permissions. Ensure that `/home/user/.ssh` and `/home/user/.ssh/authorized_keys` have the strictly correct, secure permissions required by SSH (otherwise SSH will reject legitimate logins).

**Phase 3: Payload Decoder Implementation**
We need to decode the captured C2 traffic payloads to understand what was stolen. You must write a Python script at `/home/user/decoder.py`.
1. The script must accept exactly one command-line argument: a continuous hexadecimal string representing the raw bytes of the intercepted payload.
2. The script must decode this hex string into raw bytes.
3. It must perform a byte-wise XOR operation on the payload using the integer `DECODER_KEY` you extracted from the image in Phase 1.
4. It must print the resulting decoded bytes to standard output as a UTF-8 string (ignore or replace decoding errors if necessary, but the test cases will use valid ASCII/UTF-8).
5. The script must be completely deterministic and execute silently except for the final decoded string.

Our automated testing framework will verify your `/home/user/decoder.py` by fuzzing it with thousands of random hex payloads and strictly comparing the standard output bit-for-bit against a known-good reference oracle. Ensure your implementation perfectly matches the expected XOR logic and prints nothing else.