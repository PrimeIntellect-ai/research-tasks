You are tasked with finding a regression in a Rust-based data processing pipeline located at `/home/user/data_processor`. 

Recently, we discovered an intermittent failure where the pipeline occasionally drops records during concurrent data transformation. The problem is a race condition that does not trigger on every run. 

There are approximately 200 commits in the repository. The tag `v1.0` is known to be good (no dropped records), and the branch `main` (current `HEAD`) is known to be bad.

Your task:
1. Write a bash script that reliably detects the intermittent failure. The data processor reads from an input file and writes to `output.txt`. You can compile and run the project using `cargo run`.
2. The expected output is exactly 1000 lines. The bug causes `output.txt` to occasionally have fewer than 1000 lines. Your script should run the processor multiple times (e.g., 20 times) to assert the intermediate state and catch the intermittent failure. If any run produces less than 1000 lines, the commit is bad.
3. Use `git bisect` along with your bash script to automatically find the exact commit that introduced the race condition.
4. Once you have identified the first bad commit, save its full 40-character Git commit hash to `/home/user/bad_commit.txt`.

Ensure your final commit hash is the only text in `/home/user/bad_commit.txt`. Do not leave the repository in the middle of a bisect state when you are done.