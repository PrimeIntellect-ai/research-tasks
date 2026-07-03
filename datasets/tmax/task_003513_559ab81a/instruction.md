You are an AI assistant helping a researcher model the acoustic resonance of a mechanical system as a network graph. 

The researcher has recorded the acoustic emissions of the system, which are stored in the audio file `/app/signal.wav`. The signal contains three primary resonant frequencies obscured by noise.

Your task is to:
1. **Signal Processing & Density Estimation**: Process `/app/signal.wav` to estimate the power spectral density and extract the 3 most prominent resonant frequencies (in Hz). Round these frequencies to the nearest integer.
2. **Graph Model Optimization**: The system is modeled as an undirected, fully-connected weighted graph with $N=4$ nodes (representing 4 physical masses). The acoustic frequencies correspond to the non-zero eigenvalues of the graph's Laplacian matrix $L$, scaled by a factor of 100. Let the 3 frequencies be $f_1, f_2, f_3$. We want to find a $4 \times 4$ Laplacian matrix $L$ whose eigenvalues are $0, \frac{f_1}{100}, \frac{f_2}{100}, \frac{f_3}{100}$. 
   - $L$ must be a valid Laplacian matrix: symmetric, row sums exactly 0, and off-diagonal elements $\le 0$.
   - Use optimization techniques to find the off-diagonal elements of $L$ (which define the graph's edge weights) that minimize the mean squared error between the non-zero eigenvalues of $L$ and the target scaled frequencies.
3. **Model Serving**: Create and start an HTTP server listening on `127.0.0.1:8000`. Provide a GET endpoint at `/model` that returns a JSON response in the following format:
```json
{
  "frequencies": [f1, f2, f3],
  "laplacian": [
    [L11, L12, L13, L14],
    [L21, L22, L23, L24],
    [L31, L32, L33, L34],
    [L41, L42, L43, L44]
  ]
}
```
The frequencies should be sorted in ascending order. The `laplacian` should be a 2D list of floats.

Constraints:
- You must use Python for this task.
- Ensure the server stays running in the background so it can be verified.
- The Laplacian matrix must be valid (symmetric, non-positive off-diagonals, zero row sums) to within a tolerance of $10^{-4}$.
- The eigenvalues of the Laplacian must match the scaled frequencies to within a tolerance of $10^{-2}$.