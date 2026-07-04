You are a bioinformatics analyst working on a pipeline to evaluate the properties of potential primer sequences. We have a vendored Rust crate at `/app/seq_utils` that provides basic sequence operations, including melting temperature (Tm) calculation. However, a recent commit introduced a bug, causing its scientific regression tests to fail. 

Your tasks are:
1. **Fix the vendored package**: Inspect `/app/seq_utils` and fix the `melting_temp` function so that `cargo test` passes. The Tm must be calculated using the standard Wallace rule: `Tm = 2 * (A + T) + 4 * (G + C)`.

2. **Implement an Analyzer**: Create a new Rust binary project at `/home/user/analyzer`. This project must depend on the local `/app/seq_utils` crate.

3. **Input parsing**: Your binary must read a single standard FASTA format string from standard input (stdin). It should handle a single sequence record, ignoring the `>` header line, and properly concatenating the sequence across multiple lines. You can assume the sequence will only contain uppercase `A`, `C`, `G`, `T`.

4. **Density Estimation (Histogram)**:
   - If the concatenated sequence is strictly less than 20 base pairs long, your program must output exactly the string `TOO_SHORT` (followed by a newline) and exit.
   - Otherwise, extract every contiguous 20-bp sliding window (stride of 1) from the sequence.
   - For each 20-bp window, calculate its Tm using the fixed `seq_utils::melting_temp`.
   - Compute a 10-bin histogram of these Tm values. Since a 20-bp sequence under the Wallace rule has a minimum Tm of 40 and a maximum of 80, the bins span from 40 to 80 with a width of 4.
   - The 10 bins are defined as: `[40,44), [44,48), [48,52), [52,56), [56,60), [60,64), [64,68), [68,72), [72,76), [76,80]`. Note that the final bin `[76,80]` is inclusive of 80.
   - Print the 10 integer counts separated by commas (e.g., `0,2,5,0,0,0,0,0,0,0`) to stdout.

5. **Build**: Compile your binary in release mode so the executable is located at `/home/user/analyzer/target/release/analyzer`.

Our automated fuzz-tester will pipe randomly generated FASTA sequences into your compiled binary and assert that your standard output is bit-exact equivalent to our reference oracle.