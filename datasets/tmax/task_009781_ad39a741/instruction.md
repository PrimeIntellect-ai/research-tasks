You are an AI assistant helping to curate a binary artifact repository. 

We have an incoming directory of unsorted files located at `/home/user/artifacts`. This directory contains a deeply nested structure of files, some of which are 64-bit ELF binaries, some are 32-bit ELF binaries, and some are plain text or malformed files.

Your task is to write a Rust program that acts as an artifact curator. 

Please perform the following steps:
1. Initialize a new Rust executable project at `/home/user/curator`. You may add external dependencies like `walkdir` if you wish.
2. Implement the Rust program to accept exactly two command-line arguments: a source directory and a target directory.
3. The program must recursively traverse the source directory.
4. For each file encountered, the program must determine if it is a **64-bit ELF binary**. You must do this by reading the first 5 bytes of the file. A file is a 64-bit ELF if it begins with the magic bytes `0x7F`, `0x45`, `0x4C`, `0x46` (which translates to `\x7FELF`) AND the 5th byte is `0x02` (which indicates 64-bit).
5. If a file is a 64-bit ELF, you must copy it into the target directory (do not preserve the original directory structure, just place the file directly in the target directory using its original base filename).
6. **Important Constraint (Atomic Writes):** To prevent our repository from ever seeing partially copied files during crashes, the copy operation *must* be atomic. For each valid 64-bit ELF, you must first read it and write its contents to a temporary file in the target directory named `<original_filename>.tmp`. Once the write is completely finished and the file is closed, you must atomically rename it to exactly `<original_filename>`. 
7. Build your project in release mode (`cargo build --release`).
8. Create the directory `/home/user/curated`.
9. Execute your compiled binary, passing `/home/user/artifacts` as the source and `/home/user/curated` as the target.

Do not delete or modify the original files in `/home/user/artifacts`. If two valid ELF files have the same name in different subdirectories, you can assume that overwriting in the target directory is acceptable for this scenario (though our test set has unique names).