You are an artifact manager curating a binary repository. We have received a large, critical artifact that was transmitted in multiple chunks to bypass firewall size limits. The chunks are stored in `/home/user/repo/` as `blob.parta` and `blob.partb`.

Your task is to safely reconstruct the artifact, traverse its nested archives, and verify its final contents.

Specifically, you must do the following:
1. Write a C program at `/home/user/merger.c` that takes an output filename followed by a list of input chunk filenames as command-line arguments (e.g., `./merger <output_file> <input1> <input2> ...`).
2. The C program MUST use POSIX `flock()` to acquire an exclusive lock (`LOCK_EX`) on the output file before it starts writing, ensuring no other processes can corrupt the file while it is being built. It should read the input files sequentially and append their contents to the output file, then release the lock.
3. Compile your C program and use it to merge `/home/user/repo/blob.parta` and `/home/user/repo/blob.partb` into `/home/user/repo/merged.tar.gz` (in alphabetical order).
4. The reconstructed file `merged.tar.gz` is a multi-part/nested archive. Extract it. Inside you will find an archive named `inner.zip`.
5. Verify the integrity of `inner.zip` and extract its contents to retrieve the final file `artifact.bin`.
6. Calculate the SHA-256 checksum of the extracted `artifact.bin`.
7. Create a file at `/home/user/curation_report.txt` containing exactly one line with the checksum in this exact format:
   `Artifact SHA256: <the_sha256_hash_here>`

Ensure your C program robustly handles file opening, locking, and clean up. You may use standard Linux command-line tools for the extraction and hashing steps.