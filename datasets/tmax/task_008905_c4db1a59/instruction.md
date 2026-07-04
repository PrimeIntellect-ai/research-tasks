You are tasked with helping a researcher organize and normalize a continuously growing dataset. The researcher receives data files encoded in ISO-8859-1, organized in a complex directory structure that occasionally contains accidental infinite symlink loops.

You need to write a Rust program that safely traverses the dataset directory, detects text files, converts their character encoding, and copies them to an output directory while preserving the directory structure.

Here are your specific instructions:
1. Initialize a new Rust project called `dataset_normalizer` in `/home/user/dataset_normalizer`.
2. Write a Rust program that accepts two command-line arguments: an input directory and an output directory (e.g., `cargo run -- /home/user/raw_data /home/user/processed_data`).
3. The program must recursively traverse the input directory looking for all files with the `.dat` extension.
4. **Symlink Loop Prevention:** The input directory contains a symlink loop. Your Rust program must gracefully follow symlinks but detect and avoid infinite loops (for example, by tracking the canonical paths or device/inode numbers of visited directories).
5. **Encoding Conversion:** For every `.dat` file found, read its contents assuming it is encoded in ISO-8859-1. Convert the content to UTF-8 and write it to the output directory. The output file should have the same relative path and filename as the input file, but with the extension changed to `.utf8`.
6. Compile your program and run it against the input directory `/home/user/raw_data` and output directory `/home/user/processed_data`.

To prove your program works, after running it, execute a command to write the output of `find /home/user/processed_data -type f | sort` to a file named `/home/user/result_list.txt`.