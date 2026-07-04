We are localization engineers working on updating and cleaning our large translation memory (TM) databases. As part of our ETL pipeline, we rely on a custom tool that processes raw text dumps by streaming the data, tokenizing, normalizing, and performing hash-based deduplication to give us a unique set of clean phrases.

Unfortunately, we lost the source code for this utility years ago. We only have a stripped binary located at `/app/legacy_dedup`. We need to migrate our pipeline to a new architecture, so we need a modern C++ replacement that perfectly replicates the behavior of this legacy binary.

Your task is to:
1. Treat `/app/legacy_dedup` as a black box. Feed it various text inputs (it reads from `stdin` and writes to `stdout`) to deduce its exact normalization, tokenization, and deduplication rules. Pay close attention to how it handles punctuation, casing, spacing, and empty lines.
2. Write a highly efficient C++ program that performs the exact same processing. It must be capable of handling large-file streaming (processing line-by-line without loading the entire file into memory, aside from the deduplication state).
3. Compile your final C++ program to `/home/user/new_dedup`.

Your program will be rigorously tested against the legacy binary using a fuzzer that generates thousands of random inputs to ensure bit-exact output equivalence. Make sure you handle edge cases exactly as the original binary does!