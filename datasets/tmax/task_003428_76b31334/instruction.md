**Final Target:** `/home/user/sequence_analyzer.py`
You are a bioinformatics analyst building a robust sequence processing pipeline.

1. **Context Extraction:** An image artifact is located at `/app/reference_params.png`. This image contains a handwritten note with specific numerical weights for nucleotides (A, C, G, T). Use an OCR tool (like `tesseract`, pre-installed) to extract these values.

2. **Core Implementation (`/home/user/sequence_analyzer.py`):**
Write a Python script that takes two command-line arguments: a DNA sequence string and an integer seed.
`python3 /home/user/sequence_analyzer.py <sequence> <seed>`

The script must perform the following strictly deterministic procedure:
*   Map the sequence to a numerical array using the weights extracted from the image.
*   Compute the Power Spectrum Density: Calculate the Discrete Fourier Transform (using `numpy.fft.fft`), compute the magnitude squared for each component $P[k] = |DFT[k]|^2$, and normalize it so it sums to 1 to form a probability distribution $Q[k]$.
*   Compute the Kullback-Leibler (KL) divergence (base 2) between $Q[k]$ and a uniform distribution $U[k] = 1/L$ (where $L$ is the sequence length). To avoid log(0), add $1e-9$ to $Q[k]$ before computing the divergence: $D = \sum Q[k] \log_2(Q[k] / U[k])$.
*   **Bootstrap Confidence:** Initialize `numpy.random.seed(seed)`. Perform exactly 100 bootstrap iterations. In each iteration, resample $L$ indices *with replacement*, construct the new numerical sequence, compute the KL divergence $D$, and store it.
*   **Final Output:** Sort the 100 bootstrapped $D$ values. Select the 95th percentile (which corresponds to the 95th element in the sorted array, i.e., index 94). Print this single float rounded to exactly 4 decimal places (e.g., `0.1234`).

Ensure your code handles the math exactly as specified to pass automated equivalence testing against a compiled reference binary.