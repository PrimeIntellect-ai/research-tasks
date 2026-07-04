I am a researcher running statistical simulations for primer design and sequence analysis. We recently had a server failure and lost the source code for our custom sequence alignment scoring tool. All we have left is a stripped Linux binary located at `/app/seq_align_scorer`.

I know the underlying algorithm uses a standard Needleman-Wunsch global sequence alignment between two DNA sequences provided as command-line arguments (Target and Primer), and it outputs a single integer score to standard output. However, the exact scoring parameters (match reward, mismatch penalty, and linear gap penalty) were hardcoded in the lost source, and I don't remember what they were.

Your task is to:
1. Probe and black-box test the `/app/seq_align_scorer` binary to determine the exact integer values for the match score, mismatch penalty, and gap penalty.
2. Create a new Rust project at `/home/user/rust_scorer` and reimplement the exact same scoring logic. Your program must accept two DNA sequences as command-line arguments and print only the resulting integer score to stdout.
3. Compile your Rust program in release mode. The final executable must be at `/home/user/rust_scorer/target/release/rust_scorer`.
4. Write a bash regression test script at `/home/user/test_scorer.sh` that generates at least 50 random DNA sequence pairs, runs both the legacy binary and your Rust implementation, and asserts that their outputs match exactly.

The automated test suite will aggressively fuzz your compiled Rust binary against the legacy binary using hundreds of randomly generated DNA sequences to ensure bit-exact equivalence.