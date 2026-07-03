You are tasked with building a component for a binary archive configuration tracker. The system tracks changes in compiled ELF binaries and records their states. 

An image of the physical archive tag is located at `/app/archive_tag.png`. It contains the alphanumeric Archive ID.

Write a Bash script `/home/user/archive_tracker.sh` that takes exactly one argument: the path to an input file.

Your script must perform the following:
1. **Extract the Archive ID:** Read the text from `/app/archive_tag.png` using OCR (e.g., `tesseract`). Strip any leading or trailing whitespace and newlines to get the exact Archive ID.
2. **Validate Binary Format:** Inspect the provided input file. Check if the file starts with the standard ELF magic number (`\x7fELF`).
3. **Extract Header:** 
   - If the file does not start with the ELF magic number, or if the file is smaller than 4 bytes, the extracted result should be the string `INVALID`.
   - If it is an ELF file, extract exactly the first 16 bytes of the file (the ELF `e_ident` array). If the file is smaller than 16 bytes (but at least 4), pad the remaining bytes logically with null bytes (`\x00`) so you always process exactly 16 bytes.
   - Format these 16 bytes as a lowercase, contiguous hexadecimal string (exactly 32 hex characters, e.g., `7f454c46010101...`).
4. **Output:** Print the final formatted string to standard output in the exact format:
   `<ARCHIVE_ID>|<RESULT>`
   (For example: `ARCHIVE-99|7f454c46010000000000000000000000` or `ARCHIVE-99|INVALID`)

**Requirements & Constraints:**
- Your script must be marked executable.
- The input files might be completely random binary blobs, empty files, or valid ELF files. You must use standard stream redirection, pipes, and binary-safe tools (like `head`, `xxd`, `od`) to avoid shell parsing errors on null bytes.
- Do not print any extraneous text or debug information to standard output, as it will be strictly compared by an automated equivalence verifier.
- The OCR tool `tesseract` is pre-installed in the environment.