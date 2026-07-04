You are acting as a bioinformatics analyst. We are designing DNA primers and need to filter out candidate sequences that contain hidden periodic motifs, as these cause severe off-target amplification and secondary structure issues. 

Your task consists of three main stages:

1. **Fix the Vendored Library**: 
   We have a proprietary sequence analysis library located at `/app/vendored/bio-spectrum-0.1.0`. It performs 1D domain decomposition and uses Fourier Transforms to calculate the power spectrum of DNA sequences (mapping nucleotides to numeric values and running an FFT).
   However, the source code was archived incorrectly and currently fails to compile due to a missing dependency declaration in its manifest. Identify the missing dependency (related to the FFT functionality used in the source code), fix the package, and ensure it can be compiled successfully.

2. **Develop the Filtering Tool**:
   Create a new Rust binary project at `/home/user/motif_filter`.
   This tool must depend on the local, fixed `/app/vendored/bio-spectrum-0.1.0` library.
   Your CLI must accept exactly two arguments: an input directory containing `.fasta` files, and an output directory.
   Invocation format: `cargo run --release -- <input_dir> <output_dir>` (or running the compiled binary directly).
   The tool must read all `.fasta` files in the input directory, compute their power spectrum using the `bio_spectrum::power_spectrum` function, and analyze the results. 

3. **Calibrate and Filter (Adversarial Corpus)**:
   You have been provided with two reference directories:
   - `/home/user/data/clean/` : Contains sequence files that are known to be stable and good for primer design.
   - `/home/user/data/evil/` : Contains sequences with adversarial periodic motifs that must be rejected.
   
   Analyze the spectral outputs (specifically looking for the maximum peak in the frequency spectrum, excluding the DC component at index 0) for both corpora to find a clean decision boundary threshold.
   Your tool must copy a `.fasta` file to `<output_dir>` **if and only if** it is classified as "clean". "Evil" sequences must be ignored/rejected.

Your final deliverable is the compiled binary located at `/home/user/motif_filter/target/release/motif_filter`. Automated tests will execute this binary against a mixed directory of hidden clean and evil sequences. To pass, your tool must achieve a 100% acceptance rate for clean sequences and a 100% rejection rate for evil sequences.