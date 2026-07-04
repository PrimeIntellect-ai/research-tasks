You are a bioinformatics analyst working with newly generated DNA sequence data from a novel nanopore-like sequencing platform. The sequencer's signal processing software occasionally produces anomalous reads due to adapter contamination and spectroscopic signal artifacts. 

Your task is to build a high-performance sequence sanitizer in C to filter out these anomalous sequences.

First, you must fix and compile our lab's proprietary sequence parsing library, `libfasta-parser`, which has been vendored at `/app/libfasta-parser`. Recently, a junior developer made a commit that broke the build. You must identify the error in the package, fix it, and ensure it compiles successfully into a shared library (`libfasta.so`).

Second, using this fixed library, write a C program named `sequence_sanitizer` in `/home/user/sequence_sanitizer.c` and compile it. 
Your program must read a FASTA format sequence from standard input (stdin) and output to standard output (stdout) *only* the sequences that pass all the following quality checks:
1. **Valid Alphabet:** The sequence must only contain valid IUPAC DNA characters (`A`, `C`, `G`, `T`, `N`), case-insensitive. Any sequence containing other letters (e.g., `Z`, `J`) must be rejected.
2. **Adapter Free:** The sequence must NOT contain the specific artificial primer/adapter sequence `GTCGAC` (case-insensitive).
3. **Statistical GC Content:** The sequence must have a GC content (percentage of G and C bases out of the total A, C, G, T, N bases) strictly between 35.0% and 65.0% (inclusive).

Sequences that fail ANY of these criteria must be completely omitted from the output. Sequences that pass must be printed exactly as they appeared in the input (preserving the FASTA header line starting with `>` and the sequence lines).

The verifier will test your compiled `/home/user/sequence_sanitizer` binary against two hidden corpora:
- A "clean" dataset of biologically valid sequences.
- An "evil" dataset of anomalous sequences containing the artifacts described above.

To pass, your program must process `stdin` to `stdout`, preserving 100% of the clean sequences and rejecting 100% of the evil sequences.