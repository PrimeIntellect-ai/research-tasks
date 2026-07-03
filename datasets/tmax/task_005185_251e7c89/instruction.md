I am a researcher working on organizing our lab's historical datasets. We have an old, proprietary data processing tool located at `/app/dataset_encoder`. This tool was used to prepare datasets by tokenizing strings, extracting specific features, and reducing their dimensionality into a compact representation.

Unfortunately, we lost the source code for this tool. It is a stripped Linux binary, and we need to migrate our infrastructure to Rust. Your task is to analyze the behavior of `/app/dataset_encoder` and write a replacement program in Rust that produces the exact same output for any given input.

Here is what we know about the algorithm from old documentation:
1. **Tokenization:** The input dataset is a single string (passed via standard input). The string represents a row of data, and tokens are delimited by commas (`,`).
2. **Feature Engineering:** For each token, the algorithm calculates two features:
   - The total number of bytes (length) of the token.
   - The total number of vowels in the token (both uppercase and lowercase: A, E, I, O, U, a, e, i, o, u).
3. **Dimensionality Reduction:** The algorithm reduces these two features into a single 8-bit integer (0-255). It uses a linear combination modulo 256: `(Length * C1 + Vowels * C2) mod 256`, where `C1` and `C2` are unknown positive integer constants less than 10.
4. **Output Format:** The program prints the resulting integers for each token, separated by a single space, and followed by a newline. If the input is empty or has no tokens, it might output a specific edge-case result (you should test this).

Your goals:
1. Black-box test or reverse-engineer `/app/dataset_encoder` to determine the exact values of `C1` and `C2`.
2. Write a Rust program at `/home/user/encoder.rs` that reads a string from `stdin` and outputs the identically formatted reduced feature string.
3. Compile your Rust program to an executable located at `/home/user/encoder`.

Our automated CI pipeline will fuzz-test your `/home/user/encoder` binary against `/app/dataset_encoder` using thousands of randomly generated comma-separated strings to ensure bit-exact equivalence.