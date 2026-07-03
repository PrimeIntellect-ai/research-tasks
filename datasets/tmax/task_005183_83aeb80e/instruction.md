You are an artifact manager for a secure binary repository. You need to write a strict C program that acts as a filter to curate incoming artifact bundles, accepting only legitimate bundles and rejecting malicious or corrupted ones.

First, inspect the repository policy document, which has been provided as a scanned image at `/app/policy.png`. You will need to extract the text from this image (e.g., using `tesseract-ocr` which you can install via `apt-get`) to find the exact "Magic Integrity String" required for all approved artifacts. The string will be clearly marked in the text.

Once you have the magic string, write a C program at `/home/user/artifact_filter.c` and compile it to `/home/user/artifact_filter`. Your program must take exactly one command-line argument: the path to an artifact bundle directory.

The program must perform the following checks on the given directory. If **all** checks pass, the program must exit with status code `0` (accept). If **any** check fails, or if an expected file is missing, it must exit with status code `1` (reject).

**Validation Rules:**
1. **Metadata-based file search:** The program must scan the directory to find the `.txt` file with the most recent modification time (mtime). This is the active manifest.
2. **Character encoding conversion:** The active manifest is encoded in UTF-16LE. Your C program must read it and convert its contents to UTF-8 (using the `<iconv.h>` library or similar). 
3. **Magic String Verification:** The resulting UTF-8 text must contain the exact Magic Integrity String extracted from `/app/policy.png`.
4. **Archive integrity verification:** The directory will contain exactly one `.tar.gz` file. Your program must verify that this archive is not corrupted. You may do this by invoking standard tools like `gzip -t` or `tar -tzf` via `system()` or by using a library.
5. **Symbolic link management:** The program must inspect all symbolic links within the bundle directory. If there are any symlinks, your program must resolve them (using `readlink` or `realpath`) and ensure that their targets strictly reside *within* the bundle directory. Any symlink pointing outside the directory (e.g., directory traversal `../` pointing to `/etc/passwd`) must cause the bundle to be rejected.

You have access to a test suite in `/app/corpus/clean/` (which contains valid bundles) and `/app/corpus/evil/` (which contains invalid/malicious bundles) to test your compiled `/home/user/artifact_filter` program.

You may use standard Linux commands to install dependencies, analyze the image, and test your code, but the final verifier program must be written in C and compiled as requested.