I need you to debug a regression in our mathematical C codebase. We have a custom solver for calculating 4x4 matrix transformations, located in a git repository at `/home/user/math_solver`. It has around 200 commits. Recently, a fast-path optimization introduced a bug that corrupted our query results. 

Your objectives are:
1. **Analyze the Image Fixture:** We have an image artifact at `/app/matrix_coef.png`. Use `tesseract` to extract the critical mathematical constant required for the baseline algorithm.
2. **Bisect the Repository:** Find the commit that introduced the regression in the solver. You will need to write an assertion-based validation script to test the intermediate commits. 
3. **Fix the Code:** Once you locate the regression, repair the C code using the correct constant extracted from the image and ensure corrupted inputs (e.g., NaNs or zero-determinant matrices) are handled properly via our fallback routine.
4. **Compile the Final Executable:** Produce a fully fixed binary compiled to exactly `/home/user/math_solver/bin/solver`.

The final binary must be bit-exact equivalent in behavior to our reference oracle implementation when tested across a wide distribution of inputs. Fix the logic, compile the solver, and leave it at the specified path.