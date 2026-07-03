You are a forensics analyst responding to a compromised host. We recovered a screen capture of the attacker's exfiltration process in a video file at `/app/surveillance.mp4`. The attacker encoded their authentication token as a sequence of flashing binary blocks in the video.

Your objectives:
1. **Video Analysis**: The video contains a 10x10 grid of black and white pixels in the exact center of each frame. Each frame encodes 100 bits (row-major order; black pixel = `1`, white pixel = `0`). The concatenated bits from all frames decode to an ASCII string containing a JWT token.
2. **Exploitation**: The recovered token was used to access a local Rust web service running on `http://127.0.0.1:8080`. The service is vulnerable to a cryptographic bypass: it accepts tokens where the algorithm is set to `none`.
3. **Privilege Escalation**: Modify the extracted JWT to grant yourself the `admin` role, strip the signature, and set `"alg": "none"` (or `NONE`). 
4. **Data Recovery**: Use the forged token to authenticate to `http://127.0.0.1:8080/evidence` and retrieve the hex-encoded checksum of the exfiltrated payload.

**Performance Requirement**:
We have a slow Python baseline script that extracts the video data, but we need a high-performance Rust implementation for future forensic tooling. 
Create a Rust project at `/home/user/fast_exploit/`. The compiled binary must:
- Extract the JWT from `/app/surveillance.mp4`.
- Craft the malicious `alg=none` JWT.
- Make the HTTP GET request to `http://127.0.0.1:8080/evidence`.
- Print ONLY the retrieved checksum to `stdout`.

Your Rust implementation will be tested against our Python baseline. It must achieve a runtime speedup of at least 3.0x. You may use `ffmpeg` as a subprocess or any Rust crates. Do not print anything else to standard output.