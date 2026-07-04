Hello IT Support,

We have a ticket regarding a regression in our internal Rust utility library, `tz_utils`. The library calculates local midnight timestamps, but downstream services are reporting subtle offset errors when dealing with timezones other than UTC. 

It seems a bug was introduced in the `local_day_start` function inside `/home/user/tz_utils/src/lib.rs` at some point in the recent commit history. We have a fuzzing harness set up in the repository (using `cargo fuzz`) that asserts the mathematical properties of `local_day_start`, which is currently failing on the `main` branch.

Your task:
1. Use `git bisect` combined with the fuzz test (or a custom script) to find the exact commit that introduced the bug.
2. Write the 40-character git commit hash of the bad commit into `/home/user/bad_commit.txt`.
3. Correct the formula implementation in `/home/user/tz_utils/src/lib.rs` so that it calculates the UTC timestamp of the start of the local day correctly (i.e., local midnight converted back to UTC).
4. Ensure your fix is committed to the `main` branch and that `cargo +nightly fuzz run fuzz_target_1 -- -runs=10000` passes without any panics.

Note: You might need to install `cargo-fuzz` and use the nightly toolchain to run the fuzz tests. You can install them via `cargo install cargo-fuzz` and `rustup toolchain install nightly`.

Please leave the fixed repository in `/home/user/tz_utils` on the `main` branch.