You are a performance engineer optimizing a spectroscopy analysis pipeline. The pipeline processes raw signal data, extracts the dominant spectral peaks, and evaluates the log-likelihood of various theoretical models to find the best fit. The original implementation was extremely slow and suffered from numerical underflow when evaluating the likelihood of poor models, resulting in `NaN`s and incorrect posterior estimates.

Your task is to write a highly optimized, numerically stable Python script from scratch at `/home/user/analyze.py` that does the following:

1. **Load Data**: Load the 1D signal array from `/home/user/signal.npy` (length $N$) and the array of proposed theoretical models from `/home/user/models.npy` (shape $K \times 3$).
2. **Spectral Analysis**: Compute the Fast Fourier Transform (FFT) of the signal. Normalize the FFT by dividing the results by $N$. Extract the magnitudes (absolute values) of the positive frequencies only (indices `1` to `N//2 - 1` inclusive).
3. **Peak Extraction**: Find the top 3 highest peak magnitudes in the positive frequencies. Sort these 3 magnitudes in descending order to get $M_1, M_2, M_3$.
4. **Stable Posterior Estimation**: Each row in `models.npy` represents a model $k$ containing three expected magnitudes $A_{k1}, A_{k2}, A_{k3}$. For each model, compute the log-likelihood of the extracted peaks assuming Gaussian noise with $\sigma = 0.05$. The formula for the total log-likelihood of model $k$ is:
   $$\log L_k = \sum_{i=1}^{3} \left[ -\frac{(M_i - A_{ki})^2}{2 \sigma^2} - \log(\sqrt{2\pi}\sigma) \right]$$
   *Crucial*: You must implement this directly in log-space. Do not compute the exponent and then take the logarithm, as this will cause numerical underflow for poor models.
5. **Output**: Find the integer index $k$ (0-indexed) of the model with the highest log-likelihood. Write this integer index to a file named `/home/user/best_model_idx.txt`.

Make sure your script runs efficiently and produces the correct model index.