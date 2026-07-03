You are tasked with debugging a regression in a Rust project that handles database Write-Ahead Log (WAL) recovery. 

A recent commit introduced a severe bug: when the application attempts to recover from a corrupted WAL file, it panics and crashes (resulting in a core dump) instead of gracefully returning an error. You need to find the exact commit that introduced this panic.

The repository is located at `/home/user/wal_project`. 
- The `HEAD` commit is known to be broken (panics on recovery).
- The very first commit in the repository (the initial commit) is known to be good.
- There are exactly 200 commits in this repository.
- To test a commit, you can run `cargo run -- corrupted.wal`. A good commit will exit successfully (exit code 0). A bad commit will panic (crash).
- **Warning:** Some intermediate commits have broken builds (compiler or linker errors). You must not flag a commit as the "first bad commit" if it merely fails to compile. You are specifically looking for the first commit that successfully compiles but *panics* during runtime when processing `corrupted.wal`.

Your task:
1. Use `git bisect` (and optionally a helper script) to find the first commit that introduced the runtime panic.
2. Once you find the first bad commit hash, save it to a file named `/home/user/bad_commit.txt`. 

The file `/home/user/bad_commit.txt` must contain *only* the full 40-character SHA-1 hash of the buggy commit.