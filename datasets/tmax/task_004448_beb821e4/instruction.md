You are an incident responder analyzing a suspicious artifact found on a compromised Linux server. We suspect the attacker was exfiltrating data by hiding it within audio files (steganography) and sending them over the network. 

During the initial cleanup, the attacker's extraction tool (written in Rust) was deleted from their working directory. We have a copy of the Git repository they were using, but the current working tree is empty.

Additionally, we captured an audio file they were about to send: `/app/suspicious_audio.wav`.

Your objectives are:
1. **Recover the Source Code:** Investigate the Git repository located at `/home/user/investigator_repo`. Recover the deleted Rust source code for the extraction tool.
2. **Debug the Tool:** The recovered tool is incomplete or buggy. It is supposed to extract a hidden payload from the WAV file. However, it crashes or produces incorrect results due to a signed integer overflow when calculating the sample indices. Use a debugger to find the crash, analyze the data transformation, and fix the integer overflow bug so the extraction succeeds.
3. **Build an Extraction Service:** We need to integrate this tool into our automated analysis pipeline. Wrap the fixed extraction logic in a simple HTTP server using Rust (e.g., using `hyper`, `actix-web`, or simply `std::net::TcpListener`).
   - The server must listen on `127.0.0.1:8000`.
   - It must accept an HTTP POST request to the `/analyze` endpoint. The body of the request will be the raw bytes of a WAV file.
   - The server must respond with an HTTP 200 OK and the plain-text extracted string as the body.

Please ensure your HTTP server remains running in the background once it is ready, so our automated verification script can send a test WAV file to it.