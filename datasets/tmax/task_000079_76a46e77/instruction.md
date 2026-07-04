You are an ML engineer preparing a dataset of spectroscopic signals for a matrix factorization model. Your training pipeline keeps failing because some of the input spectral matrices are near-singular (highly collinear or mostly flatline noise), which causes the factorization algorithm to diverge.

To fix this, you need to write a Bash filter script that flags these near-singular inputs. 

Here is what you have:
1. **Source Code**: A basic C program located at `/home/user/src/estimator.c` that estimates the condition number of a spectrum matrix using a power iteration method (convergence testing). You must compile this program using `gcc` to `/home/user/bin/estimator`.
2. **Calibration Image**: An image from the spectrometer hardware located at `/app/calibration.png`. You will need to extract the exact `MAX_CONDITION_NUM` and `CONV_TOL` (convergence tolerance) values from this image. `tesseract` is installed for OCR, or you can read it manually.
3. **Usage**: The compiled estimator takes the tolerance and a file path: `/home/user/bin/estimator --tol <CONV_TOL> <spectrum_file>`. It prints out a single float representing the condition number.

**Your Goal**: 
Create an executable Bash script at `/home/user/check_spectrum.sh`. 
- The script must take exactly one argument: the path to a `.spec` file.
- It must run the estimator tool on the file using the convergence tolerance found in the image.
- It must exit with code `0` if the estimated condition number is LESS THAN the maximum condition number found in the image (indicating a valid, non-singular spectrum).
- It must exit with code `1` if the condition number is GREATER THAN OR EQUAL TO the maximum condition number (indicating a near-singular, "evil" spectrum).
- It must be written using standard Bash constructs and standard CLI utilities.

Ensure your script is robust and executable, as it will be run automatically against a large corpus of clean and near-singular spectral data.