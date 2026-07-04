You are acting as a security researcher investigating a suspicious container payload. You have intercepted a corrupted custom Write-Ahead Log (WAL) file dropped by the malware at `/app/suspicious.wal`. 

We have identified that the malware uses an older open-source library to write these logs. The source code for this library, `libwalparse` (version 1.2.0), has been vendored at `/app/libwalparse`. 

Your objective is to successfully parse `/app/suspicious.wal` and extract all valid human-readable string payloads from the records. However, the situation is complicated by a few factors:
1. **Build Failures:** The vendored `libwalparse` package fails to build in our current environment. You must diagnose and fix the compiler/linker errors to install the Python extension.
2. **Corrupted Input & Integer Overflow:** The malware authors intentionally corrupted some WAL headers. When the C-extension parser hits these corrupted records, an integer overflow (specifically a signed integer issue) causes the parser to either crash or loop infinitely. You must find the flaw in the C code, patch it to gracefully skip or handle corrupted sizes, and rebuild the package.
3. **Recovery:** Once the library is robust, write a Python script at `/home/user/recover.py` that uses the `walparse` Python module to read `/app/suspicious.wal`. Extract the string payload from every successfully parsed record and write them to `/home/user/extracted.log` (one payload per line).

**Constraints & Requirements:**
- Do not use external libraries to parse the WAL; you must fix and use the vendored `libwalparse` package.
- The WAL file contains multiple valid records interspersed with maliciously crafted headers. Your goal is to recover as many valid records as possible.
- `/home/user/extracted.log` must contain purely the extracted strings, one per line.

An automated verifier will evaluate your `/home/user/extracted.log` against the known ground truth of payloads embedded in the file, scoring your extraction recall.