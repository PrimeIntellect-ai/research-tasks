You are helping a researcher organize a messy set of legacy data files. 

The dataset is located in `/home/user/dataset/` and contains nested directories with various `.log` files. 
These legacy files are encoded in UTF-16LE. 

Your task is to write a Rust program at `/home/user/process.rs` (and compile it to `/home/user/process`) that performs the following dataset organization operations:
1. Recursively traverse the `/home/user/dataset/` directory to find all `.log` files.
2. Read each `.log` file, properly decoding it from UTF-16LE to UTF-8.
3. Perform a text transformation on the content: replace all occurrences of the exact string `ERROR_CODE_99` with `RESOLVED_01`.
4. Write the transformed UTF-8 text to a new file in the `/home/user/processed/` directory. The output file should be named using the original file's basename (you can assume all basenames in the dataset are unique).
5. For each successfully processed file, create a hard link in `/home/user/links/` that points to the newly created file in `/home/user/processed/`. The hard link should have the exact same name as the file in the processed directory.

Before running your program, make sure to create the `/home/user/processed/` and `/home/user/links/` directories if they do not exist.

Ensure your Rust program compiles successfully with standard Rust tools (`rustc`). Execute your compiled program to complete the organization task.