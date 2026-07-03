You are a bioinformatics analyst tasked with preprocessing a large dataset of sequence reads. Recent batches of FASTA files have been contaminated with chimeric artifacts. You need to build a robust C-based filtering tool that accepts clean files and rejects contaminated ones.

To detect anomalies, your lab uses a custom MCMC-based posterior estimation library called `seq-mcmc` (version 1.0). This library estimates the posterior probability that a given sequence is a chimeric artifact by running parallel MCMC chains. 

Your tasks:
1. **Fix the Vendored Library**: The `seq-mcmc` library source code is located at `/app/vendored/seq-mcmc-1.0`. The previous developer attempted to add OpenMP support for parallel MCMC chain execution but broke the build configuration. Find the issue in the build setup, fix it, and compile the library to an object file or static library.
2. **Develop the Detector (`/home/user/detector.c`)**: Write a C program that uses the `seq-mcmc` library. The program must:
   - Accept exactly one argument: the path to a FASTA file.
   - Parse all sequences within the given FASTA file.
   - Evaluate each sequence using the library's `compute_artifact_posterior(const char* seq)` function. You must use OpenMP in your `detector.c` file to parallelize the scoring of multiple sequences within the file.
   - If *any* sequence in the file yields a posterior probability strictly greater than `0.80`, the file is considered contaminated.
   - Exit with code `0` if the file is clean (all sequences <= 0.80).
   - Exit with code `1` if the file is contaminated (evil).
   - Compile your program to an executable located exactly at `/home/user/detector`.
3. **Orchestrate via Notebook**: Create a Jupyter Notebook at `/home/user/pipeline.ipynb`. It must contain a bash cell that successfully compiles your `detector` (linking against the fixed `seq-mcmc` library and properly enabling OpenMP). You may also use the notebook to test your detector against the local datasets.

Local Datasets for Testing:
- Clean sequences: `/app/corpus/clean/`
- Contaminated sequences: `/app/corpus/evil/`

Ensure your final compiled executable (`/home/user/detector`) is robust. The automated verification will test your executable against an unseen adversarial corpus of evil and clean FASTA files.