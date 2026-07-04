You are a bioinformatics analyst tasked with analyzing the spectroscopic signal characteristics of a set of DNA primers. We encode DNA sequences into a numerical format (A=1.0, C=-1.0, G=2.0, T=-2.0) and use matrix decomposition (Singular Value Decomposition) to find the dominant sequence motif's strength.

You have been provided with a C++ program at `/home/user/spectral_align.cpp` that reads a list of aligned sequences, converts them into a numeric matrix $M$, computes $A = M^T M$, and uses the Power Method to find the top spectral feature.

However, the scientific regression test for this code is failing. 
There is a mathematical bug in `/home/user/spectral_align.cpp` relating to how it calculates the final singular value from the power iteration result. 

Your task:
1. Review and fix the bug in `/home/user/spectral_align.cpp`. 
2. Verify your fix by running `/home/user/test_regression.sh`. This script compiles your code and compares its output on `/home/user/reference_primers.txt` against the known ground truth in `/home/user/reference_sv.txt`.
3. Once the regression test passes, run the compiled program (`/home/user/spectral_align`) on the target dataset `/home/user/primers.txt`.
4. Save the standard output (which should be a single floating-point number formatted to 3 decimal places) to a new file named `/home/user/result.txt`.

Do not modify `test_regression.sh`, `reference_primers.txt`, or `reference_sv.txt`. You only need to fix the C++ code and generate the final `result.txt` file.