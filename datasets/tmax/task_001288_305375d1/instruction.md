Hello, we are experiencing a critical failure in our forensic analysis build pipeline. As our lead forensic developer, we need you to debug and fix the pipeline. 

The pipeline extracts artifacts from a compromised server's network capture and screen recording. However, the build is currently timing out due to a severe bug in our primary parsing script, and when we manually bypass the timeout, the floating-point calculations are incorrect.

Here are your tasks:

**Phase 1: Asset Analysis**
1. We have a packet capture located at `/app/traffic.pcap`. You need to determine the total number of TCP packets in this file.
2. We have a screen recording located at `/app/evidence.mp4`. You need to determine the exact number of frames in this video.
3. Write these two values comma-separated (e.g., `150,300`) to `/home/user/asset_counts.txt`.

**Phase 2: Script Debugging & Reverse Engineering**
Our decoding script at `/home/user/decode.sh` is supposed to process hex-encoded payload strings extracted from the pcap. However, the developer left two critical bugs in it:
1. An infinite loop/recursion bug that causes the build to hang indefinitely.
2. A floating-point precision error where values are truncated incorrectly during the normalization step.

We have an old, stripped, closed-source binary version of the decoder at `/app/reference_decoder` that operates perfectly. Unfortunately, we lost the original C source code, so we are rewriting it in Bash. 

Your goal is to fix and rewrite `/home/user/decode.sh` so that its behavior, standard output, and exit codes are **bit-for-bit identical** to `/app/reference_decoder` for *any* valid hex string input. 
- The script takes a single argument: a continuous hex string (e.g., `1A2B3C`).
- You must use delta debugging, manual testing, or reverse engineering of the `/app/reference_decoder` binary to understand exactly how the floating-point math and loop logic is supposed to work, and replicate that logic in your Bash script.
- Ensure your script gracefully handles loop termination and outputs the exact same floating-point precision format as the reference binary.

The automated verification will fuzz your `/home/user/decode.sh` script against `/app/reference_decoder` with hundreds of random hex strings to ensure absolute equivalence.

Good luck.