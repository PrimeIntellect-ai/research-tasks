I have an old project backup system that produced custom single-file archives, but I lost the original extraction script. I found a screenshot of my old design notes at `/app/format_spec.png` which describes the exact custom binary format, including a specific magic header, a byte-level obfuscation key, and the compression algorithm used.

Please write a Python script at `/home/user/decompress.py` that can read these custom archive files and print their decompressed contents to standard output. 

Your script must accept exactly one command-line argument: the path to the custom backup file.
Example invocation:
`python3 /home/user/decompress.py /tmp/sample.bkp > /tmp/output.dat`

The script needs to:
1. Read the binary file.
2. Validate and strip the magic header (as specified in the image).
3. Reverse the byte-level obfuscation (as specified in the image).
4. Decompress the payload to recover the original binary data.
5. Write the exact recovered binary data to `stdout`.

Make sure to analyze the image carefully to understand the extraction steps, as my backups depend on this exact sequence.