You are a Machine Learning Engineer preparing a dataset of Markov Chain Monte Carlo (MCMC) traces for training a generative model. 

The data comes from a network of sensors monitoring a complex physical system. However, several sensors have lost calibration and are producing "evil" data—traces that have drifted from the system's true posterior distribution. Your objective is to build a classifier that filters out these corrupted traces.

To know the *true* posterior distribution, you must refer to a scanned lab notebook from the lead physicist, located at `/app/lab_notes.png`. 
1. Use OCR (e.g., `tesseract`) to extract the text from this image.
2. The note describes a system of two non-linear equations. Solve this system to find the unique root in the first quadrant ($x > 0, y > 0$). This root represents the **mean** ($\mu$) of the target Gaussian posterior distribution.
3. The note also specifies that the **precision matrix** (the inverse of the covariance matrix, $\Sigma^{-1}$) is defined by the Jacobian of that exact system of equations, evaluated at the root.
4. Using matrix inversion/decomposition techniques (like Cholesky or SVD), derive the expected covariance matrix $\Sigma$ of the true distribution.

You must write a Python script at `/home/user/classifier.py`.
- It must take a single command-line argument: the path to a CSV file containing an MCMC trace (with headers `x,y`).
- Your script must estimate the sample mean and sample covariance of the trace.
- If the sample mean and sample covariance match the theoretical $\mu$ and $\Sigma$ (derived from the lab note) within a reasonable tolerance (e.g., absolute difference $\le 0.4$ for all elements), the script must print exactly `CLEAN` to standard output.
- Otherwise, it must print exactly `EVIL`.
- The script must exit with code 0.

You have access to a set of trace files to test your assumptions if needed. The true test will be run by an automated grading system against a holdout dataset. Make sure your script handles standard CSV parsing properly and requires no interactive input.