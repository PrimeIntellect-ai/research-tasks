You have been given access to a local Git repository at `/home/user/db-exporter`. This repository contains a Rust CLI tool designed to query a database and export the results to a custom binary format (`output.bin`).

Recently, a regression was introduced somewhere in the commit history (there are 200 commits in total). At the oldest commit, running `cargo run -- export` produces an `output.bin` that perfectly matches the reference file located at `/home/user/expected.bin`. However, at the current `HEAD`, the generated `output.bin` is corrupted due to an encoding and serialization bug. The system fails to correctly write out the binary data for some query results.

Your task is to:
1. Identify the exact Git commit that introduced the regression. 
2. Save the full, 40-character Git commit hash of this "bad commit" to `/home/user/bad_commit.txt`.
3. Fix the bug in the current `HEAD` commit (do not checkout the old commit permanently; leave the repo at `HEAD` with your fix applied).
4. Run `cargo build --release` and then run `/home/user/db-exporter/target/release/db-exporter export` to generate a new `output.bin` in the repository root.
5. Ensure that the newly generated `/home/user/db-exporter/output.bin` exactly matches `/home/user/expected.bin`.

You will need to use your debugging skills to trace the binary serialization bug and leverage tools like `git bisect` to locate the regression. Writing a minimal test script to automate the bisect process is highly recommended.