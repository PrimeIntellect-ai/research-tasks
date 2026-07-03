You are an AI assistant helping a technical writer organize a large set of documentation. The writer received a proprietary binary archive file named `/home/user/docpack.bin` from a third-party vendor. However, the vendor's archive format is known to be vulnerable to "Zip Slip" style attacks, where maliciously crafted file paths in the archive can overwrite files outside the intended extraction directory.

Your task is to safely extract the documentation, sanitize it, and prepare it for publishing.

**Step 1: Safe Extraction Utility (C++)**
Write a C++ program at `/home/user/extract.cpp` that reads `/home/user/docpack.bin` using high-performance streaming or memory-mapped I/O (`<sys/mman.h>` or `std::ifstream::read`).
The `docpack.bin` file uses a custom binary format:
1. Starts with a 4-byte magic header: `DOCP`
2. Followed by a sequence of file entries. Each entry consists of:
   - Path Length: 2 bytes, unsigned little-endian integer (`uint16_t`)
   - File Path: ASCII string of length specified above.
   - Content Length: 4 bytes, unsigned little-endian integer (`uint32_t`)
   - Content: Raw bytes of length specified above.

Your C++ program must extract the contents into the directory `/home/user/docs_safe/`.
**Security Constraint:** To prevent directory traversal attacks, your program must silently **skip** (do not extract) any entry whose File Path contains the substring `../`. 
For valid entries, extract the file to `/home/user/docs_safe/<File Path>`. You may assume `std::filesystem::create_directories` can be used to handle any needed subdirectories.

Compile and run your C++ program to perform the extraction.

**Step 2: Large-Scale Text Editing**
The extracted documentation contains a placeholder `[COMPANY_NAME]` that needs to be updated.
Using standard shell utilities (like `find`, `xargs`, `sed`), perform an in-place find-and-replace on all `.md` files within `/home/user/docs_safe/` (and its subdirectories) to replace every occurrence of the exact string `[COMPANY_NAME]` with `AcmeCorp`.

**Step 3: Verification Manifest**
Generate a manifest file at `/home/user/manifest.txt` that lists all the files successfully extracted and retained in `/home/user/docs_safe/`.
The manifest should contain the relative paths of the files (e.g., `intro.md`, `api/setup.md`), one per line, sorted alphabetically.

Ensure all steps are executed and the final state matches these requirements exactly.