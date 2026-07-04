You are an artifact manager maintaining a local binary repository of compiled packages. Recently, an automated system crashed while splitting a large custom archive, scattering binary chunks across the `/home/user/artifacts/` directory tree. Worse, security scans flagged this archive format for a "zip slip" vulnerability because the internal file paths contain malicious `../` directory traversal sequences.

Your task is to reconstruct the archive, write a C utility to safely parse and sanitize its internal file table, and prepare the files for a safe bulk import.

Here are your instructions:
1. **Analyze the Image Fixture:** There is a screenshot of the original archiver's configuration at `/app/archive_map.png`. Use an OCR tool (like `tesseract`) to read it. It contains a `CHUNK_PREFIX` string and a `MAGIC_SIG` header value.
2. **Merge the Chunks:** Recursively search `/home/user/artifacts/` for all files matching the `CHUNK_PREFIX`. Sort them alphanumerically by their current filenames, and merge them into a single file at `/home/user/reconstructed.bin`.
3. **Write a C Sanitizer:** Create a C program at `/home/user/sanitizer.c` and compile it to `/home/user/sanitizer`. The `reconstructed.bin` file begins with the `MAGIC_SIG` (as a string), followed by a newline, and then a list of null-terminated file paths. Your C program must:
   - Read `reconstructed.bin`.
   - Verify the `MAGIC_SIG`.
   - Read each null-terminated path.
   - Strip out any `../` or `..` directory traversal components to make the path strictly relative to the current directory (e.g., `../../usr/lib/foo.so` becomes `usr/lib/foo.so`).
   - Write the cleaned, null-terminated paths to `/home/user/clean_paths.bin`.
4. **Prepare Bulk Rename Map:** Use `awk` or `sed` to read `clean_paths.bin` (treating nulls as separators) and output a text file at `/home/user/rename_map.txt` containing the mapping in the format: `original_corrupted_path -> cleaned_path` (separated by a newline).

Your solution's correctness will be evaluated by an automated test script that measures the exact string-match accuracy of your sanitized paths against a hidden reference set.