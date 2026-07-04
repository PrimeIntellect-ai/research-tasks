You are an MLOps engineer building a high-performance C++ tool to track and validate dimensionality-reduced experiment artifacts (PCA embeddings) stored in a large-scale binary backend. 

Currently, your validation pipeline is failing. We use a vendored, lightweight CSV parser located at `/app/csv-parser-2.1.3` to read our artifact metadata. However, the package has a deliberate perturbation: its `Makefile` is broken (it attempts to build with `-std=c++98`, but the library requires C++17).

Your tasks are:
1. Fix the `Makefile` in `/app/csv-parser-2.1.3` so it correctly compiles with `-std=c++17`. Run `make` inside the directory to produce `libcsvparser.a`.
2. Write a C++ program in `/home/user/workspace/artifact_filter.cpp` that statically links against `libcsvparser.a` and uses its headers.
3. The program must be compiled to an executable named `/home/user/workspace/artifact_filter`.

The `artifact_filter` executable must take exactly two command-line arguments:
`./artifact_filter <metadata.csv> <embeddings.bin>`

**Multi-source Data Joining & Validation Logic:**
The program must read the CSV file (which has a header) and join it with the binary file.
The CSV format is: `id,expected_dim,offset,length`
- `id`: string (the artifact identifier)
- `expected_dim`: integer (the expected number of dimensions / features)
- `offset`: integer (byte offset in `embeddings.bin` where this artifact's vector starts)
- `length`: integer (number of bytes to read from `embeddings.bin` for this artifact)

The binary file contains single-precision (4-byte) IEEE 754 little-endian floats.

For each artifact in the CSV, validate the corresponding vector from the binary file. An artifact must be marked as `REJECT` if ANY of the following are true:
- The `length` in bytes does not match `expected_dim * 4`.
- Any floating-point value in the vector is NaN (Not a Number) or Infinity.
- The L2 norm of the vector is exactly 0.0.

If none of the above are true, mark the artifact as `ACCEPT`.

**Output Format:**
Your program must print its results to standard output (`stdout`), printing one line per artifact ID in the same order they appeared in the CSV, formatted exactly as:
`<id>,ACCEPT`
or
`<id>,REJECT`

We have provided two test corpora at `/data/clean_corpus/` and `/data/evil_corpus/`. Each contains a `metadata.csv` and an `embeddings.bin`. The automated verifier will compile your code and run your executable against both corpora. You must successfully ACCEPT 100% of the valid artifacts in the clean corpus, and REJECT 100% of the corrupted artifacts in the evil corpus.