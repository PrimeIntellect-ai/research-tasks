You are an engineer investigating issues in a long-running Bash service located in the Git repository at `/home/user/repo`. 

There are two distinct problems to solve:
1. **Memory Leak**: The `service.sh` script currently suffers from a memory leak because it continuously appends data to an array inside its main loop without ever clearing it. You need to identify the exact Git commit that introduced this memory leak. The first commit in the repository is known to be "good" (no leak).
2. **Secret Exposure**: A previous developer accidentally committed an AWS-style API token to a file named `config.sh` in the repository's history, but later removed it. You need to perform Git forensics to recover this secret token.

Your final goal is to report your findings. Create a file at `/home/user/solution.txt` with exactly two lines:
- The first line must be the full 40-character Git commit hash that introduced the memory leak.
- The second line must be the exact secret API token recovered from the Git history (just the token value itself, e.g., `AKIA...`).

Ensure you do not alter the current `HEAD` of the repository in your final state (if you use `git bisect`, remember to `git bisect reset` when done).