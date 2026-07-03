You are tasked with tracking down a regression in a Go CLI tool using `git bisect`.

The repository is located at `/home/user/go-parser`. The tool processes a file called `input.csv` which occasionally contains malformed or corrupted records. Previously, the tool handled these gracefully. However, a recent commit introduced a regression: when the tool processes an input file containing a corrupted record, it intermittently panics. Because of the intermittent nature of the bug, a single execution of `go run main.go input.csv` may succeed even if the code contains the bug.

Your objective is to find the exact commit that introduced this regression.

Instructions:
1. The repository currently has its `HEAD` on the latest commit (which is broken).
2. The initial commit in the repository is known to be good.
3. You will need to write a small shell script to wrap the Go execution so that `git bisect run` (or your manual bisection) can reliably identify whether a commit is "good" or "bad" despite the intermittent nature of the failure. Running the script 20-30 times per commit should be sufficient to force the failure if the bug is present.
4. Once you have identified the 40-character SHA-1 hash of the *first bad commit* (the commit that introduced the intermittent panic), save it to `/home/user/bad_commit.txt`.

Ensure `/home/user/bad_commit.txt` contains *only* the 40-character commit hash, with no trailing newline or extra text.