A researcher is organizing a massive collection of dataset directories. Unfortunately, some untrusted datasets downloaded from external sources contain corrupted data files and malicious symlink structures that crash our automated backup system.

We have a legacy stripped binary at `/app/legacy_checker` that was previously used to detect corrupted data files. It takes a file path as an argument and exits with code 1 if the file is corrupted, or 0 if it is clean. However, it is too slow to run on our entire cluster, doesn't handle directory traversal, and crashes when it encounters symlink loops.

Your task is to write a fast, robust Rust utility that acts as a dataset sanitizer. It must accept a single directory path as a CLI argument, recursively traverse the directory, and exit with code 1 (reject) if the directory contains ANY of the following "evil" traits:
1. An infinite symlink loop (e.g., A -> B -> A, or a link pointing to its own parent).
2. A corrupted data file. You must reverse-engineer or analyze the black-box `/app/legacy_checker` binary to determine exactly what binary format or header it considers "corrupted", and implement that exact check natively in your Rust code.

If the directory is completely safe (no symlink loops and no corrupted files), your utility must exit with code 0 (accept).

You are provided with two corpora for testing:
- `/app/corpus/clean/` contains safe dataset directories.
- `/app/corpus/evil/` contains malicious dataset directories.

Create your Rust project at `/home/user/dataset_filter`. Your final executable must be compiled in release mode and located at `/home/user/dataset_filter/target/release/dataset_filter`.