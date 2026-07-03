You are tasked with recovering steganographic data from a captured video stream (`/app/evidence.mp4`). The data was exfiltrated by a malicious actor who hid a binary sequence in the luminance channel of the video.

We recovered the attacker's extraction tool in `/home/user/steg_extractor`. However, the tool is a legacy Python 2 package with a C extension. We are now running a strict Python 3 environment, and the tool is broken. Additionally, the original C extraction algorithm is too naive and fails due to compression noise in the video.

Your objectives:

1. **Migrate Build System & Code:** 
   - Fix `/home/user/steg_extractor/setup.py` so it builds cleanly under Python 3 (e.g., using `setuptools`).
   - Refactor the C extension in `/home/user/steg_extractor/steg.c`. You must update the Python 2 C API calls (like `PyString_` and `initsteg`) to their Python 3 equivalents (`PyBytes_` and `PyInit_steg`). 
   - Fix the Python driver script `/home/user/steg_extractor/process.py` to be Python 3 compatible.

2. **Improve the Numerical Algorithm in C:**
   - The current `extract_bit` function in `steg.c` attempts to read the hidden bit by simply looking at the least significant bit (LSB) of the absolute top-left pixel `frame[0]`. Compression artifacts destroy this LSB.
   - The payload was actually encoded as a strong luminance shift in the entire top-left 10x10 pixel block.
   - Modify the C algorithm to compute the average luminance (pixel value) of the top-left 10x10 block of the frame. Return `1` if the average is strictly greater than 127, otherwise return `0`. (Assume the input frame is an array of raw 8-bit grayscale pixels).

3. **Compile and Run:**
   - Install the package locally (`pip install -e .` or similar).
   - Use `ffmpeg` to extract the frames of `/app/evidence.mp4` at exactly 10 frames per second. Convert them to raw 8-bit grayscale (`gray` pixel format) and pipe them to the `process.py` script. The video is exactly 640x480 resolution.
   - The `process.py` script should process each frame sequentially and output a single continuous string of 1s and 0s.
   - Save this output string into `/home/user/output.txt`.

Ensure `/home/user/output.txt` contains only the continuous string of extracted bits (e.g., "101100101...") with no trailing newlines or other text.