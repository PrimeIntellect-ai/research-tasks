You are a bioinformatics analyst working on a sequence evolution project. We need to estimate the transition/transversion ratio ($\kappa$) from a set of aligned nucleotide sequences using Markov Chain Monte Carlo (MCMC) sampling.

Your task is to write a C program that performs this analysis. 

1. **Audio Notes**: The lead researcher left a voice memo at `/app/lab_note.wav`. You will need to transcribe it (you can install and use command-line transcription tools like `openai-whisper` via python) to retrieve the required MCMC hyperparameters:
   - The prior distribution range for $\kappa$ (Uniform distribution).
   - The proposal distribution standard deviation.
   - The total number of MCMC iterations.
   - The number of burn-in iterations to discard.

2. **Data Processing**: 
   - Read the HDF5 file located at `/app/alignments.h5`. It contains a single 2D integer dataset named `/sequences` with dimensions $100 \times 50$ (100 sequences, each 50 bases long). 
   - The nucleotides are encoded as integers: 0 = A, 1 = C, 2 = G, 3 = T.
   - Calculate the total number of transitions ($N_{ts}$) and transversions ($N_{tv}$) by comparing adjacent sequences in the dataset (i.e., compare row 0 with row 1, row 1 with row 2, ..., row 98 with row 99). 
   - A transition is a mutation between Purines (A $\leftrightarrow$ G) or between Pyrimidines (C $\leftrightarrow$ T).
   - A transversion is any other mutation (e.g., A $\leftrightarrow$ C, A $\leftrightarrow$ T).
   - Ignore positions where the bases are identical.

3. **MCMC Implementation**:
   - Write a C program (e.g., `mcmc_kappa.c`) that implements a Metropolis-Hastings MCMC sampler to estimate the posterior distribution of $\kappa$.
   - The likelihood function for $\kappa$ given the counts is:
     $L(\kappa) = \left( \frac{\kappa}{\kappa + 2} \right)^{N_{ts}} \times \left( \frac{1}{\kappa + 2} \right)^{2 \cdot N_{tv}}$
   - The prior for $\kappa$ is the Uniform distribution specified in the audio note. If a proposed $\kappa$ falls outside this range, its prior probability is 0 (reject immediately).
   - Use a Gaussian proposal distribution: $\kappa_{new} \sim \mathcal{N}(\kappa_{current}, \sigma^2)$, using the $\sigma$ from the audio note.
   - Start the chain at $\kappa = 2.0$.
   - Calculate the acceptance ratio: $\alpha = \min\left(1, \frac{L(\kappa_{new}) \times P(\kappa_{new})}{L(\kappa_{current}) \times P(\kappa_{current})}\right)$.

4. **Output**:
   - Calculate the mean of the $\kappa$ values from the MCMC chain *after* discarding the burn-in period.
   - Print this single float value (rounded to 3 decimal places) to a file named `/home/user/kappa_estimate.txt`.

Ensure your C program is compiled correctly linking against the HDF5 C libraries (`libhdf5-dev` is available/installable).