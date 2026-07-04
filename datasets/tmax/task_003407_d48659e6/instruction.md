You are an artifact manager tasked with securely curating a set of binary repositories. You have been provided with an incoming directory of compressed artifacts and a visual rule sheet.

Your workflow must accomplish the following:
1. **Read Curation Rules**: There is an image at `/app/curation_rules.png`. Extract the text from this image using OCR (e.g., `tesseract`). It contains a banned file extension that must not be included in the final curated artifacts.
2. **Secure Extraction**: Inside `/home/user/incoming_artifacts/`, there are multiple `.zip` files. Some of these archives are malicious and contain "zip slip" payloads (files that attempt to extract outside the target directory using `../`). You must write a script (in Python, Ruby, or another language) to extract these archives into `/home/user/curated_artifacts/`. If a file path within an archive attempts to escape the extraction directory, you must safely skip that specific file but extract the rest.
3. **Filtering**: Do not extract any files that match the banned extension found in the curation rules.
4. **Concurrent Registry**: As files are safely extracted, your script must update a shared JSON registry file at `/home/user/registry.json`. Since you should process the archives concurrently to save time, you must use proper file locking (e.g., `fcntl.flock` in Python) to ensure atomic writes to the JSON registry. The registry should be a flat JSON array of the extracted file paths (relative to the curated directory).
5. **Final Archival**: Once extraction and registration are complete, compress the entire `/home/user/curated_artifacts/` directory and the `/home/user/registry.json` into a single highly optimized tarball at `/home/user/final_archive.tar.xz`. You must use extreme compression settings to ensure the output file size is as small as possible.

**Constraints:**
- Do not extract to paths outside `/home/user/curated_artifacts/`.
- Ensure your script gracefully handles concurrent writes to the registry file.
- The automated test will measure the size in bytes of `/home/user/final_archive.tar.xz`. It must be minimized.