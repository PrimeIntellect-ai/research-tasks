You are a security researcher analyzing a suspicious Go-based mathematical generator tool used for producing cryptographic nonces. Recently, a vulnerability was disclosed where the generated sequence becomes predictable and weak, but it is unknown exactly when this flaw was introduced into the project.

The repository is located at `/home/user/nonce-gen`. 
The known "good" state (secure) is at the git tag `v1.0`. 
The current `master` branch `HEAD` is known to be in a "bad" (vulnerable) state.

When you run the binary with the seed `42` (i.e., `./nonce-gen 42`), the good version outputs `7831452`. The bad version outputs `11244` due to a mathematical flaw introduced in a specific commit.

Your objective is to find the exact commit hash that introduced this mathematical flaw. 

However, you will face a few hurdles:
1. The project relies on a build script (`build.sh`) that attempts to format and compile the Go code. Recently, a developer renamed a directory to include a space (`crypto core/`), which causes the naive `build.sh` to fail with a build error.
2. In the most recent commits, a dependency conflict was introduced in `go.mod` making the project fail to compile out of the box. You will need to resolve this to test `HEAD`.
3. Because the build script and dependencies might be broken at various points in the commit history, you will need to carefully orchestrate your `git bisect` process (for example, by writing a robust wrapper script that fixes the build/dependencies on the fly, or by skipping untestable commits, though the bad commit itself *is* compilable if you fix the space issue).

Once you have identified the first bad commit that altered the mathematical output for seed `42` to `11244`, write the full 40-character SHA-1 hash of that commit into a file named `/home/user/bad_commit.txt`.

Constraints:
- Only standard Linux terminal tools, bash, git, and Go are available.
- You must write the output exactly as requested to `/home/user/bad_commit.txt`. Do not include any other text in that file.