You are a red-team operator managing a command-and-control (C2) server. The blue team has discovered your listener and is actively sending probe payloads to uncover your backend infrastructure. You need to create an ingress filter that perfectly separates legitimate beacons from adversarial probes.

The previous operator left a screen recording of the initial C2 configuration in `/app/setup_recording.mp4`. You will need to extract frames from this video to recover the `SECRET_HMAC_KEY` that was temporarily printed to their terminal during setup. You have `ffmpeg` installed to assist with this.

Incoming C2 requests are intercepted as text files. Each file contains a single Base64-encoded string. Once decoded, the payload string strictly follows this format:
`BASE64_ENCODED_CLIENT_CERTIFICATE|HMAC_SHA256_HEX|COMMAND_STRING`

To be considered a valid, clean beacon, the payload MUST meet ALL of the following criteria:
1.  **Certificate Validation:** The decoded client certificate (PEM format) must be mathematically valid and signed by our Root CA located at `/app/ca.pem`.
2.  **Token Validation:** The `HMAC_SHA256_HEX` must perfectly match the HMAC-SHA256 hash of the `COMMAND_STRING`, using the `SECRET_HMAC_KEY` extracted from the video as the cryptographic key.

Any payload failing *either* of these checks, or failing to decode properly, is a blue-team probe (evil) and must be rejected.

Your objective is to write an executable script (in any language you choose, e.g., Python, Bash) at `/home/user/c2_ingress`. This script must accept a single argument: the absolute path to a file containing a payload. 
- If the payload is perfectly valid (a legitimate beacon), your script must exit with status code `0`.
- If the payload is invalid (a blue team probe), your script must exit with a non-zero status code (e.g., `1`).

For your testing and iterative refinement, I have provided a corpus of known good payloads in `/app/corpora/clean/` and a corpus of known probes in `/app/corpora/evil/`. Your script must properly classify 100% of these files.

Begin.