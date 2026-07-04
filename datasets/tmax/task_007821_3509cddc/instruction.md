You are a developer tasked with tracking down a subtle regression in a Rust-based physics engine. 

A recent release has started producing inaccurate trajectory calculations due to a precision loss bug introduced somewhere in the commit history. The repository is located at `/home/user/physics_engine`.

The `v1.0` tag represents a known good state of the code. The current `HEAD` (which is about 200 commits ahead of `v1.0`) is known to be bad.

Your task:
1. Use `git bisect` (or a custom script) to find the exact commit that introduced the precision loss regression.
2. The program is executed via `cargo run -- <time_in_seconds>`. 
3. Run the program with a time value of `10000.0` (`cargo run -- 10000.0`). 
4. The bug causes the calculated distance to diverge from the `v1.0` output by a small amount (precision loss due to a formula implementation error). Any commit that diverges from the `v1.0` expected output by more than `0.01` is considered a "bad" commit.
5. Once you find the first bad commit, save its full 40-character commit hash to `/home/user/bad_commit.txt`.

Ensure your final answer in `/home/user/bad_commit.txt` contains exactly the commit hash and nothing else.