You are a bioinformatics analyst working with a codebase that models sequence transition probabilities. 

There is a FASTA file located at `/home/user/data/input.fasta` containing several DNA sequences. 
Previously, a C++ program was used to read this FASTA file, calculate a $4 \times 4$ transition probability matrix $M$ (for bases A, C, G, T in that exact order) for each sequence, and directly compute $(M^T M)^{-1} M^T b$ where $b = [1, 1, 1, 1]^T$. 

However, this matrix factorization fails catastrophically (yielding NaNs or exceptions) because some sequences in our new dataset are highly degenerate (e.g., containing only A and T), resulting in near-singular or completely singular transition matrices.

Your task is to build a robust hybrid C++/Python workflow to handle this properly using Bayesian inference.

**Step 1: C++ Matrix Extraction**
Write a C++ program at `/home/user/src/extract_matrices.cpp`. 
It must read `/home/user/data/input.fasta`. For each sequence, calculate the $4 \times 4$ empirical transition probability matrix $M$. 
- A transition is counted from position $i$ to $i+1$. 
- Normalize each row so it sums to 1. If a base never appears, its entire row should be exactly $0$.
- The output should be saved to `/home/user/data/matrices.json`, which should be a JSON object mapping the sequence ID (without the `>`) to its $4 \times 4$ matrix (a list of 4 lists).
- Compile and run this C++ program. You may install and use libraries like `nlohmann-json3-dev` if you wish.

**Step 2: Environment & Notebook Orchestration**
Create a Jupyter Notebook at `/home/user/analysis.ipynb`. You must set up your own Python environment, installing any necessary libraries (e.g., `jupyter`, `numpy`, `emcee`, `scipy`).

**Step 3: MCMC & Bootstrap Implementation**
In your notebook, load `matrices.json`. For each sequence matrix $M$:
Instead of direct inversion, we use a Bayesian model: $\log P(\theta | M) \propto - \frac{1}{2} ||M\theta - b||_2^2 - \frac{\lambda}{2} ||\theta||_2^2$
where $b = [1, 1, 1, 1]^T$ and the ridge prior parameter $\lambda = 0.1$. $\theta$ is a 4-dimensional vector.

1. Implement an MCMC sampler (e.g., using `emcee` or a custom Metropolis-Hastings algorithm) to sample from this posterior distribution of $\theta$.
2. Draw 10,000 samples and discard the first 2,000 as burn-in.
3. Isolate the samples for the **first component** ($\theta_0$, corresponding to base 'A').
4. Calculate the empirical mean of these $\theta_0$ samples.
5. Compute a 95% Bootstrap confidence interval for this mean using 1,000 bootstrap resamples of your post-burn-in MCMC samples.

**Step 4: Output**
The final cell of your notebook must write a JSON file to `/home/user/results.json` with the following structure:
```json
{
  "Seq1": {
    "mean": 0.123,
    "ci_lower": 0.110,
    "ci_upper": 0.135
  },
  ...
}
```
Run your notebook completely from end-to-end via the command line (e.g., using `jupyter nbconvert --to notebook --execute /home/user/analysis.ipynb`).