I am a researcher running Monte Carlo simulations of a particle detector. We need to validate our simulated event distributions against an analytical baseline model using a robust distance metric.

I have an image of our detector's baseline response specification located at `/app/baseline_model.png`. This image contains text specifying the baseline analytical model, which follows a Poisson distribution, along with its precise $\lambda$ (lambda) parameter.

Your task is to:
1. Extract the $\lambda$ parameter from `/app/baseline_model.png`.
2. Write a Python script at `/home/user/compute_kl.py` that computes the Kullback-Leibler (KL) divergence between an empirical input distribution and this baseline Poisson distribution.

The script `/home/user/compute_kl.py` must meet the following exact specifications to pass our automated numerical stability tests:
- It will be invoked with a single command-line argument: a comma-separated list of non-negative floats representing empirical counts for sequential bins $k=0, 1, 2, \dots, N-1$. (Example: `python3 /home/user/compute_kl.py 1.5,2.0,0.0,4.1`)
- **Numerical Stability for Input ($P$)**: Parse the input array. If any count is strictly less than $10^{-9}$, clamp it to exactly $10^{-9}$. Then, normalize this array so its sum is exactly 1.0. This normalized array is your distribution $P$.
- **Analytical Baseline ($Q$)**: For bins $k=0$ to $N-1$, calculate the unnormalized baseline probability using the Poisson probability mass function with the $\lambda$ you found in the image: $Q_{raw}(k) = \frac{\lambda^k e^{-\lambda}}{k!}$.
- **Numerical Stability for Baseline**: If any $Q_{raw}(k)$ is strictly less than $10^{-9}$, clamp it to exactly $10^{-9}$. Then, normalize the $Q_{raw}$ array so its sum is exactly 1.0. This normalized array is your distribution $Q$.
- **Distance Metric**: Compute the KL divergence $D_{KL}(P || Q) = \sum_{k=0}^{N-1} P(k) \ln\left(\frac{P(k)}{Q(k)}\right)$, using the natural logarithm.
- **Output**: The script must print only the final KL divergence value to standard output, rounded and formatted to exactly 6 decimal places (e.g., `0.123456`). Do not print any other text.

Ensure your script handles edge cases smoothly. You can install tools like `tesseract-ocr` and libraries like `pytesseract` to read the image if necessary.