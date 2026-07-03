You are an artifact manager tasked with curating a custom binary repository. 

A large binary archive file is located at `/home/user/repository.bin`. This file contains multiple concatenated binary artifacts. You need to write a C++ program to parse this archive, extract and decode the artifacts, and then use standard bash tools to identify specific artifacts.

The format of `/home/user/repository.bin` consists of a sequence of artifact records. Each record has the following structure:
1. **Magic Header**: 4 bytes, ASCII string `"ARTF"`
2. **Artifact ID**: 12 bytes, ASCII hex string (e.g., `"000000000001"`)
3. **Data Size**: 4 bytes, little-endian unsigned 32-bit integer (`uint32_t`), representing the size of the payload.
4. **Data Payload**: `Size` bytes of data. The data has been obfuscated using a simple XOR cipher with the key `0x42`.
5. **Footer**: 4 bytes, ASCII string `"DONE"`

Your objectives:
1. Write a C++ program (e.g., `extractor.cpp`) to parse `/home/user/repository.bin`.
2. For each record, read the payload, deobfuscate it (XOR each byte with `0x42`), and save the decrypted payload to a file in the directory `/home/user/extracted/`.
3. The extracted file must be named `<Artifact ID>.bin` (e.g., `000000000001.bin`).
4. **Important**: You must use atomic writes when creating the extracted files to prevent partial reads by concurrent processes. Write the data to a temporary file first (e.g., `<Artifact ID>.tmp`), and then rename it to the final `<Artifact ID>.bin` filename using standard C/C++ or POSIX rename functions.
5. After running your C++ extraction program, use standard Linux shell tools (`grep`, `awk`, etc.) to search through the extracted `.bin` files. Find all artifacts whose decrypted payload contains the exact ASCII text `"CONFIRMED"`.
6. Output the Artifact IDs (just the 12-character ID, one per line, sorted alphabetically) of the matching artifacts to `/home/user/confirmed.txt`.

Constraints:
- Do not use Python or other scripting languages for the extraction logic; use C++ for the extraction tool.
- Ensure `/home/user/extracted/` exists before extracting.
- You have access to standard build tools like `g++`.