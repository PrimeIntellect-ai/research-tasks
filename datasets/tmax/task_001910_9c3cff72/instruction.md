You are a security researcher analyzing a suspicious binary used by a newly discovered malware strain. The stripped executable is located at `/app/oracle_decoder`. It reads a custom binary payload from standard input, decodes it, and writes the result to standard output.

During a recent raid, we recovered a screenshot from the malware author's workstation. This image is located at `/app/config_snippet.png`. It contains the magic constants required to properly initialize the decoding routine. 

Your objective is to reverse-engineer the behavior of the `/app/oracle_decoder` and write a functionally identical, bit-exact equivalent in Python at `/home/user/clean_decoder.py`. We need this Python implementation to deploy in our honeypots to emulate the malware's communication protocol.

Here are your specific tasks:
1. **Analyze the Configuration Image:** Use OCR (e.g., `tesseract` is installed) to extract the `MAGIC_SEED` and `XOR_KEY` from `/app/config_snippet.png`. 
2. **Reverse-Engineer the Payload Format:** Through experimentation, determine how the binary processes standard input. It expects a specific binary serialization format (likely involving a length prefix and an encoded body).
3. **Isolate the Architecture Bug:** The original malware author compiled this for a 32-bit x86 system. Our preliminary analysis indicates that the binary suffers from a 32-bit signed integer overflow when calculating the decoding offsets for payloads over a certain size. When this overflow occurs, the binary falls back to a secondary decoding path or fails in a predictable way. 
4. **Develop the Equivalent Decoder:** Write `/home/user/clean_decoder.py`. Your script must read raw bytes from `sys.stdin.buffer` and write the decoded raw bytes to `sys.stdout.buffer`. 
    * Since Python uses arbitrary-precision integers, you will need to manually implement the 32-bit signed integer overflow mechanics to perfectly mirror the oracle's buggy behavior.
    * You must ensure encoding and serialization of the byte stream exactly matches the C-style handling in the oracle.

Our automated verification system will fuzz your `/home/user/clean_decoder.py` against `/app/oracle_decoder` with thousands of randomized byte streams to ensure exact behavioral equivalence, including the edge cases where the integer overflow is triggered.

Make sure your final script is executable and has exactly the correct behavior for all inputs.