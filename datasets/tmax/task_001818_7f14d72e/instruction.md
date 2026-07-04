You are an AI assistant helping a technical writer organize and migrate old documentation. 

I have a nested archive of old documentation drafts located at `/home/user/old_docs.tar.gz`. 
If you extract this, you will find it contains a ZIP file (`internal_drafts.zip`), which in turn contains a directory filled with files bearing the `.xrd` extension (e.g., `file_01.xrd`, `file_02.xrd`).

These `.xrd` files are text documents that were obfuscated by a legacy proprietary system using a simple byte-wise XOR cipher with the hexadecimal key `0x2F`. 

Your task is to:
1. Extract the nested archives to access the `.xrd` files.
2. Write and execute a **C++ program** that reads each `.xrd` file, applies the XOR cipher (key `0x2F`) to decrypt it back to readable text.
3. As part of your C++ processing (or using standard Linux text processing tools afterward), perform a bulk text replacement: replace every instance of the exact string `[CONFIDENTIAL_DRAFT]` with `[PUBLIC_RELEASE]`.
4. Save the decrypted and modified files into a new directory: `/home/user/published_docs/`.
5. Bulk rename the output files so that an original file named `file_XX.xrd` is saved as `section_XX.md` in the new directory.
6. Create a log file at `/home/user/migration_log.txt` that lists the absolute paths of all the successfully created `.md` files in `/home/user/published_docs/`, sorted alphabetically, one per line.

Ensure that the final `.md` files contain the exact decrypted, modified text.