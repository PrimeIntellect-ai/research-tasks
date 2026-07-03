As an incident responder, you are investigating a recent data breach. We suspect a rogue insider used a custom malware binary to exfiltrate sensitive HTTP session tokens. A surveillance camera captured the compromised terminal during the exfiltration process.

We have recovered two artifacts:
1. `/app/exfil_video.mp4` - A video recording of the terminal. The malware flashes base64-encoded chunks of an encrypted payload on the screen.
2. `/app/suspicious_service` - The malware executable found on the compromised machine.

Your objective is to automate the extraction and decryption of these exfiltrated tokens by writing a Bash script at `/home/user/analyze_exfil.sh`.

The script must accept exactly two arguments:
`./analyze_exfil.sh <path_to_video> <path_to_malware>`

Your script must perform the following steps:
1. **Video Extraction & OCR**: Extract the frames from the provided video (e.g., using `ffmpeg`) and use optical character recognition (e.g., `tesseract`) to read the base64 chunks from the screen.
2. **Payload Decoding**: Concatenate the extracted text in order of appearance, ignoring whitespace and OCR noise as much as possible, and base64-decode it into an encrypted binary file.
3. **Sandboxed Execution**: The malware binary dynamically generates the encryption keys when executed, but it is destructive and attempts to connect to a C2 server. You must execute the binary *safely* inside your script using `bwrap` (Bubblewrap). Ensure it has no network access (`--unshare-net`) and that the filesystem is read-only (except for a temporary minimal tmpfs if needed). When run in this isolated state, it will fail its network check and print the keys to stdout in the format: `KEY: <hex_string>` and `IV: <hex_string>`.
4. **Decryption**: Use `openssl` to decrypt the payload. The algorithm is `aes-256-cbc`.
5. **HTTP Header Inspection**: The decrypted payload is a plaintext file containing raw HTTP requests. Parse the file and extract the value of the `Session-Token` cookie from the headers of each request.
6. **Output**: Print only the extracted `Session-Token` values to standard output, one per line.

Ensure your script is robust and handles temporary files cleanly. We will test your script against a held-out dataset of 5 similar videos and malware binaries to evaluate its accuracy.