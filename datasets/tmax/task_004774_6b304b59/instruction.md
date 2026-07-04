Hello IT Support,

Ticket #8821: We have a critical issue with our custom forensic evidence hasher, `fxhash`. 

Our security tools rely on this utility to generate deterministic checksums of forensic artifacts. However, after a recent series of updates, `fxhash` has started producing incorrect checksums for larger files. We suspect a formula implementation error (possibly related to integer boundaries or types) was introduced in a recent commit.

Additionally, a recent pull request merged into `main` has completely broken the build due to a Go module dependency conflict.

Here is what you need to do:
1. Navigate to the repository at `/home/user/fxhash_repo`.
2. Fix the dependency conflict in `go.mod` so that the project successfully compiles again.
3. We have provided the last known good compiled version of the tool at `/app/fxhash_legacy`. This is a stripped binary without source code, but you can use it as a reference oracle.
4. Use `git bisect` (or any other debugging method) comparing the repo's historical commits against the output of `/app/fxhash_legacy` to find the exact commit that introduced the hashing regression.
5. Once you understand what went wrong, fix the formula implementation in the current `main` branch.
6. Compile your corrected Go code and place the final executable at `/home/user/fxhash_fixed`.

The `fxhash` utility takes data via standard input (`stdin`) and prints a single integer string (followed by a newline) to `stdout`.

An automated verification system will heavily fuzz your `/home/user/fxhash_fixed` binary against the legacy `/app/fxhash_legacy` binary with a wide range of input lengths and bytes. They must be bit-exact equivalent in behavior.