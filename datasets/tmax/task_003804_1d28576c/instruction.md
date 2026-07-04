You are a red-team operator developing an evasion payload generator to communicate with a newly deployed, proprietary Command and Control (C2) server. We have successfully retrieved a compiled binary of the C2's payload encoder, but we need a standalone Python version to integrate into our broader toolkit. 

Your objective is to write a Python script that exactly replicates the binary's encoding algorithm. We have a whiteboard snapshot from the C2 developers stored at `/app/c2_notes.png` which contains the specific cryptographic parameters you need.

Write a Python script at `/home/user/encoder.py` that implements the following pipeline:
1. Read raw binary data from standard input (`sys.stdin.buffer`).
2. Perform a byte-wise XOR operation on the input data using the `XOR_KEY` written in the image.
3. Encode the XORed result using a custom Base64 alphabet. Standard Base64 uses `A-Z, a-z, 0-9, +, /`. The proprietary C2 uses the shifted custom alphabet explicitly listed as `ALPHABET` in the image.
4. Print the final encoded string to standard output (no trailing newline).

To successfully evade detection, your implementation must be bit-exact equivalent to the original C2 encoder. Our automated test suite will aggressively fuzz your script with hundreds of random binary inputs to ensure its output perfectly matches the reference implementation. 

Ensure your script handles standard input and output correctly, and make sure any necessary dependencies (like `Pillow` or `pytesseract` if you need them to read the image) are installed using pip. Tesseract is already available on the system.