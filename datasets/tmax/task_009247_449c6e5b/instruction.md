You are a support engineer tasked with collecting diagnostics for a failing telemetry decoder. 

Customers are reporting that the C-based telemetry decoder in `/home/user/telemetry_decoder` has started crashing (Segmentation fault) sporadically since a recent update when processing specific edge-case binary payloads. 

The application reads exactly 8 bytes of binary data from standard input. The first 4 bytes represent the sensor ID (which must be non-zero), and the last 4 bytes represent the sensor value (both as 32-bit unsigned little-endian integers). A recent commit introduced an encoding/precision bug by casting the sensor value to a `float` internally, which loses precision for certain large integers and ultimately triggers a hard crash.

Your task is to:
1. Use `git bisect` (or manual investigation) in the `/home/user/telemetry_decoder` repository to find the exact Git commit hash that introduced the crash.
2. Create a minimal reproducible example (MRE). Fuzz or manually craft an 8-byte binary file that triggers this exact segmentation fault when fed to the compiled `main.c` of the bad commit. 

Write your findings to the following locations:
- **`/home/user/bad_commit.txt`**: This file must contain exactly the full 40-character Git commit hash of the bad commit (no extra text or newlines).
- **`/home/user/mre.bin`**: This file must be exactly 8 bytes long and trigger the segmentation fault when piped into the decoder: `./decoder < /home/user/mre.bin` (assuming `decoder` is compiled from the bad commit).

*Note: You may need to compile the C code during your investigation (`gcc main.c -o decoder`). The repository history is small, and the crash requires both a non-zero sensor ID and a specifically large sensor value that loses precision when cast to a 32-bit float.*