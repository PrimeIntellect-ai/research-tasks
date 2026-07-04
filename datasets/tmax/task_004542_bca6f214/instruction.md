You are tasked with debugging a numerical instability issue that was recently introduced into a simulation codebase. The developer was in the middle of bisecting the regression across 200 commits but accidentally deleted the test script from their working disk image and lost the simulation parameters.

Here are your instructions:
1. We have mounted an ext4 filesystem image at `/app/workspace.img`. The developer accidentally deleted a file named `test_runner.py` from the root of this filesystem. Recover this deleted file and place it at `/home/user/test_runner.py`.
2. The simulation parameters were saved in an image at `/app/equation.png`. Use OCR (e.g., `tesseract`) to extract the parameters `ALPHA` and `BETA` from this image.
3. A Git repository containing the simulation codebase is located at `/home/user/sim_repo`. There are about 200 commits. An older commit works perfectly, but a recent commit introduced a floating-point precision regression (intermittent numerical instability causing the simulation to drift).
4. Inspect the recovered `test_runner.py` to understand how to test the code. You will need to plug in the `ALPHA` and `BETA` parameters you extracted.
5. Find the exact commit hash that introduced the numerical instability. Write the full 40-character commit hash to `/home/user/bad_commit.txt`.
6. Fix the precision issue. The bug typically involves catastrophic cancellation or improper accumulation of floating-point values. You must write the corrected implementation to `/home/user/fixed_algo.py`. 

The `fixed_algo.py` script must:
- Read a single line of space-separated floating-point numbers from standard input.
- Process them using the correct algorithm (with the extracted `ALPHA` and `BETA`).
- Print the final resulting floating-point state to standard output (a single number).

We will run extensive fuzz-testing against your `fixed_algo.py` using our internal reference oracle to ensure bit-exact equivalence for all edge cases.

Ensure your script is robust and properly handles floating-point summation to avoid any precision loss.