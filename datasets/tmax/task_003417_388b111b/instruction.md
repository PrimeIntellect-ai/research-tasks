You are a bioinformatics analyst working on a pipeline to estimate the true GC content distribution of a sequenced organism.

We have a FASTA file of sequence reads at `/app/reads.fasta`, and a custom C program source code for calculating sequence statistics at `/app/seq_stats.c`.

Your task is to:
1. **Compilation**: Compile the C program `/app/seq_stats.c` using `gcc` into an executable at `/app/seq_stats`.
2. **Data Processing**: Run `/app/seq_stats` on `/app/reads.fasta`. The program will output the GC fraction of each sequence, one per line. Save this output to `/app/gc_data.txt`.
3. **Image Extraction**: We received an image `/app/gel_band.png` from a collaborator that contains the prior parameters for our Bayesian model. Use OCR (e.g., `tesseract`) to read the text in this image. It contains a string like "PRIOR_MU=X, PRIOR_SIGMA=Y". Extract these two floating-point values.
4. **MCMC Sampling**: Write a Python script that implements a Metropolis-Hastings sampler to estimate the posterior of the mean GC content ($\mu$). 
   - Model the data likelihood as $X_i \sim \mathcal{N}(\mu, 0.05^2)$.
   - Model the prior as $\mu \sim \mathcal{N}(PRIOR\_MU, PRIOR\_SIGMA^2)$ using the values from the image.
   - Sampler details: 
     - Initialize $\mu_0 = PRIOR\_MU$.
     - Run 10,000 iterations.
     - Proposal distribution: $\mu_{prop} \sim \mathcal{N}(\mu_{current}, 0.01^2)$.
     - Use `numpy.random.seed(42)` right before the loop. Generate the proposal, then the uniform random variable for acceptance, in that order for each step.
   - Discard the first 1,000 iterations as burn-in. Calculate the posterior mean from the remaining 9,000 samples.
5. **Service**: Create and run a Python HTTP server listening on `127.0.0.1:9090`. It must expose:
   - `GET /prior_params`: Returns a JSON response with the extracted priors, e.g., `{"mu": 0.4, "sigma": 0.1}`.
   - `GET /posterior_mean`: Returns the posterior mean of $\mu$ calculated from the MCMC samples (excluding burn-in), as plain text rounded to 4 decimal places (e.g., `0.4512`).

Keep the HTTP server running in the background or foreground so we can verify the endpoints.