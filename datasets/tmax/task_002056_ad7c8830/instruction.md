You are a localization engineer tasked with modernizing a legacy translation pipeline. We have an old proprietary localization text encoder provided as a stripped, UPX-packed Linux binary located at `/app/loc_encoder`. This binary is used to encode UTF-8 strings into a specific internal binary format used by our custom game engine, but it is slow and crashes on certain edge cases. 

We need to rewrite this encoder in Python to integrate it directly into our modern CI/CD pipeline. 

Your task is to reverse-engineer the behavior of the `/app/loc_encoder` binary and write a completely equivalent Python script located at `/home/user/loc_encoder.py`. 

Your Python script must:
1. Accept exactly one command-line argument: the raw UTF-8 string to be encoded (e.g., `python3 /home/user/loc_encoder.py "Héllo World"`).
2. Perform exactly the same Unicode normalization, length calculations, padding, and binary framing as the original binary.
3. Output the raw encoded bytes directly to standard output (`sys.stdout.buffer`), with no extra newlines or debugging text.

You are encouraged to use `objdump`, `strings`, `gdb`, or simply treat the binary as a black box and run it with various inputs to deduce its encoding rules (pay attention to character encodings, byte endianness, padding lengths, and how it handles missing or special characters). 

Our automated verification system will extensively random-fuzz your `/home/user/loc_encoder.py` script against the original `/app/loc_encoder` binary using thousands of randomly generated multi-language strings to ensure bit-exact equivalence.