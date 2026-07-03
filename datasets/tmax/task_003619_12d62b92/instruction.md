You are tasked with organizing and deduplicating a large project dataset using high-performance C programming.

The dataset is located in `/home/user/dataset/` and contains thousands of binary files. Many of these files are exact duplicates, and they need to be categorized based on their contents and metadata.

**Step 1: Fix and Compile xxHash**
We have vendored the source code for the `xxHash` library in `/app/xxHash-0.8.2`. 
1. The `Makefile` in this package has been corrupted with an invalid compiler specification. Find and fix the perturbation.
2. Compile the package to produce the static library `libxxhash.a`.

**Step 2: Build the Organizer**
Write a C program at `/home/user/organizer.c` that does the following:
1. **Deduplication**: Scan `/home/user/dataset/`. Use `mmap` to stream file contents efficiently and hash them using the `XXH64` function from your compiled `libxxhash`. Whenever duplicate files are found (matching sizes and hashes), retain one physical copy and replace the other duplicates with **hard links** to the retained file to save disk space.
2. **Categorization**: Read the configuration file `/home/user/rules.csv`. Each line is formatted as `CategoryName,MinSizeBytes,MagicBytesHex` (e.g., `Images,1024,89504E47`).
3. After deduplicating, evaluate each unique file. If its size is `>= MinSizeBytes` and its first bytes match the `MagicBytesHex`, create a **symlink** to it in `/home/user/categories/<CategoryName>/<Filename>`. (Create the category directories if they do not exist).

**Requirements & Constraints:**
- Your C code must be compiled with `gcc` and statically link against `/app/xxHash-0.8.2/libxxhash.a`.
- Use the headers from `/app/xxHash-0.8.2/`.
- Ensure you set appropriate permissions (e.g., `0755`) when creating directories.
- Run your compiled program to execute the full deduplication and categorization workflow.

An automated verifier will evaluate the resulting directory structure, calculating a combination metric of disk space saved vs. the theoretical maximum savings, as well as the accuracy of the symlinks. You must achieve a combined score of at least 0.95.