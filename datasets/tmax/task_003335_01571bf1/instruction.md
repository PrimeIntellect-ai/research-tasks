A researcher in our lab has left, leaving behind a massive nested dataset compressed in a proprietary format. They wrote a custom C utility to extract, clean, and write out these files, but they only left a stripped compiled binary located at `/app/dataset_normalizer`. We need to integrate this tool into our new data pipeline, which is strictly written in Rust.

Your task is to reverse-engineer the behavior of `/app/dataset_normalizer` and write a bit-exact equivalent implementation in Rust. 

Here is what we know about the tool:
1. It is invoked as: `/app/dataset_normalizer <input_archive> <output_file>`
2. It reads a custom binary archive format, extracts the compressed streams, decompresses them, and applies a specific text macro/replacement to clean the dataset.
3. It safely writes the final concatenated output to `<output_file>` using a temporary file and an atomic rename to prevent partial reads by other pipeline processes.

You need to:
1. Analyze the `/app/dataset_normalizer` binary (you can use tools like `strace`, `ltrace`, `strings`, `xxd`, or construct test files to observe its behavior).
2. Deduce the binary header format, compression method, text transformations, and atomic write mechanism.
3. Write a Rust program at `/home/user/normalizer.rs` that replicates this behavior exactly.
4. Compile your Rust program to an executable at `/home/user/normalizer`.

Your final compiled binary must accept the exact same arguments and produce the exact same output files as the original tool for any valid input archive. We will test your binary against the original using an automated fuzzer.