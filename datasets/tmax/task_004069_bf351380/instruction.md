We have a Rust-based data processing tool located in `/home/user/tlv_parser` that parses custom binary TLV (Type-Length-Value) files. Recently, our data pipelines started hanging indefinitely when processing certain batches of files. We suspect a regression was introduced somewhere in the last 200 commits.

The input data samples are located in `/home/user/samples/`. There are 50 binary files in this directory. One or more of these files currently causes the parser to enter an infinite loop (acting like a deadlock in our processing thread pool) when run on the latest `master` branch.

Your task is to:
1. Identify which sample file causes the parser to hang.
2. Use git bisection on the `/home/user/tlv_parser` repository to find the exact commit hash that introduced the infinite loop bug.
3. Write the full 40-character commit hash of the offending commit to `/home/user/bad_commit.txt`.
4. Analyze the parsing logic and the offending file to find the specific edge-case format record causing the infinite loop. Extract *only* that single minimal TLV record (Type, Length, and Value) and save it as a raw binary file to `/home/user/minimal_crash.bin`. This file must be a minimal reproducible example that triggers the bug on the bad commit.

The tool is built and run via standard `cargo` commands (e.g., `cargo run -- <file_path>`).

Make sure your final outputs are exactly placed in `/home/user/bad_commit.txt` and `/home/user/minimal_crash.bin`.