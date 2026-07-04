A researcher in our lab has collected thousands of custom telemetry datasets compressed into a proprietary archive format called "DSAR" (Data Stream Archive). We need a fast parser to safely read the headers of these archives and generate extraction manifests. 

Unfortunately, the original specification document was lost, but we found a screenshot of the format definition at `/app/format_spec.png`.

Your task is to write a Python 3 script at `/home/user/parser.py` that reads a DSAR archive and prints a manifest of safely extractable files.

Requirements for `/home/user/parser.py`:
1. It must be an executable script (`chmod +x`).
2. It must accept exactly one command-line argument: the path to the DSAR file.
3. It must use memory-mapped I/O (`mmap` module) to read the archive file.
4. It must parse the archive header and records exactly as described in `/app/format_spec.png`.
5. **Security (Zip Slip Prevention):** As datasets come from untrusted sources, you must silently skip any file record whose path starts with `/` or contains `../` anywhere in the path. Do not print anything for these records.
6. For each valid (safe) record, print exactly one line to `stdout` in the following format:
   `Valid: <file_path> | Offset: <offset> | Size: <size>`

You must rely on your OCR/vision tools to read `/app/format_spec.png` to understand the magic bytes, endianness, and structural layout of the DSAR format. Do not create the test datasets yourself—we have an automated evaluation suite that will feed your script thousands of dynamically generated DSAR files and compare its output bit-for-bit against a reference implementation.

Please ensure your script is robust against malformed paths as described, handles the binary format exactly according to the schema in the image, and uses `mmap`.