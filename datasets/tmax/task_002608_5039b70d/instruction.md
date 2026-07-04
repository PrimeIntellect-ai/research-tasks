You have been tasked with recovering and organizing a developer's messy project backup. The previous developer left behind an archive, `/app/project_backup.tar`, which is known to be problematic. It contains heavily nested archives, a chaotic web of symlinks (some of which intentionally loop back on themselves to trap naive crawlers), and custom-compressed files.

Here is your workflow:

1. **Safe Extraction & Traversal:** Extract `/app/project_backup.tar`. You must safely traverse the extracted directory tree. Detect and ignore any symlinks that lead to infinite loops or point to parent directories.
2. **Nested Archives:** Find and extract any nested `.zip` or `.tar.gz` archives you encounter during traversal.
3. **Custom Decompression:** There are several `.enc` files in the tree. These have been encrypted using a simple single-byte XOR cipher. The developer left a sticky note with the key, which was scanned and saved as an image at `/app/note.png`. You will need to extract the key from this image (e.g., using `tesseract` OCR) and write a Python script to decode all `.enc` files into `.txt` files.
4. **Merge and Deduplicate:** Collect all valid `.txt` files (both the ones originally in the archive and the decoded `.enc` files). Sort them alphabetically by their base filename. Merge their contents sequentially into a single file, `/home/user/merged.txt`. As you merge, perform line-level deduplication (remove duplicate lines across the entire merged content, preserving only the first occurrence of each line).
5. **Final Compression:** Compress `/home/user/merged.txt` using maximum gzip compression and save it as `/home/user/clean.gz`.

We will measure your success by the final file size of `/home/user/clean.gz`. To pass, your implementation must successfully recover the data, properly deduplicate the lines, and produce an output file size that falls below our target threshold.