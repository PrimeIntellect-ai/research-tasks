You are a security auditor investigating a compromised file upload service. The attackers left behind a customized upload handler binary and a voicemail describing their backdoor.

Your tasks:
1. **Audio Analysis**: Transcribe and analyze the audio file at `/app/voicemail.wav` to understand the nature of the backdoor and the encoding mechanism used by the attackers. (You may use available tools like `whisper` or Python libraries to transcribe it).
2. **ELF Analysis & Reverse Engineering**: Analyze the ELF binary located at `/app/upload_handler`. Based on the instructions in the voicemail, locate and extract the secret decryption key embedded within the binary. 
3. **Detector Implementation (Rust)**: Write a Rust program that acts as a filter for incoming upload filenames.
   - The program must take a single command-line argument: the path to a file containing a raw byte payload (the encoded filename).
   - It must decode the payload using the exact mechanism and key extracted from the binary.
   - It must analyze the decoded filename for path traversal attacks. Specifically, any decoded string that contains `../` or starts with `/` should be considered malicious.
   - If the payload is **malicious** (evil), the program must terminate with **exit code 1**.
   - If the payload is **safe** (clean), the program must terminate with **exit code 0**.
   - Compile your Rust program to the exact path `/home/user/detector`.

An automated verification suite will test your compiled `/home/user/detector` against a large corpus of both safe and malicious payloads. You must ensure your Rust program is efficient and correctly handles all edge cases in the decoding process.