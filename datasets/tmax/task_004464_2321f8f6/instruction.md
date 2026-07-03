You have inherited an unfamiliar Bash-based data processing codebase located at `/home/user/data_pipeline`. This pipeline is responsible for generating processed images based on specific formulas and intermediate text configurations. 

Recently, two major issues were reported:
1. **A Regression in Serialization:** At some point in the commit history, a bug was introduced where intermediate config files are generated with the wrong text encoding, causing downstream `awk` commands to fail or produce garbage.
2. **Incorrect Formula:** The final processing step (which applies a transformation based on an equation) is producing the wrong visual results. The previous developer left a screenshot of their handwritten notes containing the correct mathematical formula at `/app/dev_notes.png`.

Your objectives are:
1. **Information Extraction:** Use OCR (e.g., `tesseract`, which is pre-installed) to read the contents of `/app/dev_notes.png`. You will find the correct parameters for the scaling formula.
2. **Git Bisection:** Use `git bisect` in `/home/user/data_pipeline` to find the exact commit that introduced the encoding/serialization bug. The script `process.sh` should execute without throwing "invalid byte sequence" or producing empty outputs when given a standard ASCII input.
3. **Debugging and Fixing:**
   - Fix the encoding bug (which might involve correcting an `iconv` command or standardizing output formats).
   - Update the math formula in `process.sh` (or its associated `awk` script) to match the formula recovered from the image.
4. **Pipeline Execution:** Run the fixed pipeline script `./process.sh /home/user/input_data.dat` to generate the final image at `/home/user/final_output.png`.
5. **Regression Test:** Create a script at `/home/user/test_regression.sh` that takes an input data file as an argument, runs the pipeline, and exits with `0` if the output is correctly formatted and generated without errors, or `1` otherwise.

Your final success will be evaluated based on the Structural Similarity Index (SSIM) of your generated `/home/user/final_output.png` against a hidden reference image, which requires both the encoding fix and the exact formula from the notes to be perfectly implemented.