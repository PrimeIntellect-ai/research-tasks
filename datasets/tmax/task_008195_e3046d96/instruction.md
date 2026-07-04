I am a bioinformatics analyst running a sequence processing pipeline. I have a C++ program `/home/user/spectral_analysis.cpp` that reads a DNA sequence from `/home/user/sequence.fasta`. It maps the nucleotides to numerical values (A=1.0, C=2.0, G=-1.0, T=-2.0), computes the Discrete Fourier Transform (DFT) magnitudes of this signal, and calculates a total "spectral energy" score by summing these magnitudes. 

Recently, we've noticed precision loss and non-reproducible results when scaling this algorithm to larger sequences in our parallel system. The issue originates from using standard single-precision `float` and naive loop summation, which introduces floating-point reduction errors.

Your task is to fix the script to ensure highly deterministic and precise numerical behavior:
1. Modify `/home/user/spectral_analysis.cpp` to use **`double`** precision instead of `float` for all signal storage, trigonometric calculations, and magnitude variables (`signal`, `re`, `im`, `angle`, `mag`, and `total_magnitude`).
2. Replace the naive `total_magnitude += mag;` accumulation step with a strict **Kahan summation** algorithm to properly mitigate floating-point accumulation errors.
3. Compile your modified C++ script. You can use standard tools available in the environment (e.g., `g++ -O2 spectral_analysis.cpp -o spectral_analysis`).
4. Run the compiled executable and redirect its standard output to `/home/user/result.txt`. The output must be exactly the final sum formatted to 6 decimal places (the existing code already has `std::setprecision(6)`).

The FASTA file and the base C++ code are already present in `/home/user`. Do not change the underlying DFT math logic or the numerical mappings, only upgrade the precision and the summation method.