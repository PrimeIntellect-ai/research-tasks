You are a backup administrator tasked with retiring a legacy data archiving utility that is no longer maintained. The original utility is provided as a compiled, stripped Linux binary located at `/app/legacy_extract`. 

Your objective is to write a Python 3 script at `/home/user/extract.py` that perfectly replicates the behavior, output, and file operations of this legacy tool. 

**Background & Requirements:**
1. The legacy tool takes a single argument: the path to a custom archive file (e.g., `backup.arc`).
2. When executed, it extracts the contents of the archive into the current working directory.
3. **Link Management (Deduplication):** To save disk space, if multiple files within the archive have exactly the same content, the utility writes the first encountered file normally. For all subsequent identical files, it creates a **hard link** to the first file instead of writing the redundant data to disk.
4. **Manifest Generation & Format Conversion:** After processing the archive, the utility converts the internal binary metadata into a structured JSON manifest and prints it strictly to standard output (`stdout`). 
5. The JSON manifest must contain a sorted list of all processed files, their SHA-256 checksums, and their creation type (`original` or `hardlink`, including the link target).

**Testing Your Solution:**
You have full access to `/app/legacy_extract`. You can generate sample `.arc` files (you will need to reverse-engineer or black-box test the binary to understand the exact byte-structure of the `.arc` format) to observe its filesystem actions and standard output. 

Your Python replacement must be functionally identical. An automated verifier will generate thousands of random `.arc` files containing various combinations of unique and duplicate files, passing them to both `/app/legacy_extract` and your `/home/user/extract.py`. Your script's `stdout` output must be bit-for-bit identical to the legacy tool, and the resulting filesystem state (including inodes/hard links) must match perfectly.

Write your final implementation at `/home/user/extract.py`. You may use any standard Python libraries.