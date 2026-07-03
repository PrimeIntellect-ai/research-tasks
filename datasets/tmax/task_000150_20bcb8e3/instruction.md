You have been tasked with recovering and organizing old project logs that were compressed using a custom archive format by a former developer. This developer was dealing with log rotation race conditions and built a custom archiver, but the only surviving documentation for the format is a screenshot of their notes located at `/app/specs.png`.

Additionally, some of these log files were corrupted due to race conditions during writing (truncation/tearing), or they were injected with malicious SQL payloads during a past security incident.

Your objective is to write a Go command-line tool that acts as a filter and integrity checker for these custom archive files.

Requirements:
1. Examine the image `/app/specs.png` (using OCR tools like `tesseract`, which is preinstalled) to extract the specifications of the custom compression format. The specs will define the magic header bytes, the compression algorithm used, the integrity verification method (trailer format), and a specific blacklist string that indicates a malicious payload.
2. Write a Go program at `/home/user/sanitiser.go` and compile it to `/home/user/sanitiser`.
3. The compiled binary must accept exactly one argument (the file path to evaluate):
   `./sanitiser <path_to_archive>`
4. The program must:
   - Read the binary archive.
   - Verify the magic header exactly matches the specification.
   - Decompress the payload according to the specified algorithm.
   - Verify the uncompressed data's integrity using the specified checksum method.
   - Ensure the uncompressed text does NOT contain the blacklist string.
5. Exit Codes:
   - If the file is perfectly valid, intact, and safe (clean), the program MUST exit with code `0`.
   - If the file has a wrong header, fails decompression (due to race condition truncation), fails the integrity checksum, or contains the blacklisted string (evil), the program MUST exit with code `1`.

Make sure your Go code handles all edge cases cleanly without panicking (a panic resulting in a non-zero exit code is acceptable for an evil file, but graceful handling is preferred).