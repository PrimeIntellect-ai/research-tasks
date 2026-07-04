You are an operations engineer triaging a critical incident in our proprietary financial anomaly detection pipeline. The pipeline relies on a legacy, stripped compiled binary for fast numerical operations, but it has started crashing frequently with out-of-memory errors and segmentation faults.

Here is what you need to do:

1. **Dependency Resolution**: The original Python environment was lost. There is a `/app/requirements.txt` file, but installing it fails due to a dependency conflict between `numpy`, `scipy`, and an older pinned package. Resolve the conflicts and install the dependencies in your local user environment so the pipeline can run.
2. **Code Repair**: The Python wrapper `/app/wrapper.py` interfaces with the binary. It currently suffers from a convergence failure in its iterative data-smoothing loop and an off-by-one boundary condition that truncates the last column of the input matrices. Diagnose and fix these bugs directly in `/app/wrapper.py`.
3. **MRE Creation & Binary Analysis**: The core math is done by a stripped binary located at `/app/matrix_eig_solver.bin`. Create a minimal reproducible example script to feed matrices to this binary. You will discover that certain mathematical properties in the input data cause the binary to infinite-loop or crash.
4. **Sanitizer Development**: We have captured a dataset of historical inputs. 
   - Known good inputs are in `/app/corpus/clean/`
   - Inputs that crash the system are in `/app/corpus/evil/`
   Write a standalone Python script at `/home/user/sanitizer.py` that takes a single file path as a command-line argument. The script must parse the JSON matrix, determine if it is "clean" or "evil" based on the mathematical flaw you identified in the binary, and return exit code `0` if the file is safe to process, or exit code `1` if it should be rejected.

Your `sanitizer.py` will be tested against the hidden full corpora. It must achieve 100% acceptance on the clean corpus and 100% rejection on the evil corpus.