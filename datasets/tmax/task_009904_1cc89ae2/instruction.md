I am a researcher working on optimizing PCR primers for a multiplex assay. I have generated a set of candidate primer sequences, but I need to analyze the distribution of their GC contents to ensure they fall within the optimal range. 

I have a FASTA file located at `/home/user/primers.fasta` containing these candidate primer sequences. 

Please perform the following analysis using Python:
1. Parse the `/home/user/primers.fasta` file and calculate the GC content for each sequence. The GC content should be calculated as the percentage of 'G' and 'C' bases out of the total length of the sequence (e.g., a value between 0.0 and 100.0).
2. Fit a Gaussian Kernel Density Estimate (KDE) to this 1D array of GC percentages. Use `scipy.stats.gaussian_kde` with its default bandwidth selection (Scott's Rule).
3. Determine the probability that a primer drawn from this estimated continuous distribution has an optimal GC content, which we define as being strictly between 40.0% and 60.0%. To do this, use numerical integration (`scipy.integrate.quad`) to integrate the KDE's Probability Density Function (PDF) from 40.0 to 60.0.
4. Write the final probability, rounded to exactly 4 decimal places, to a file named `/home/user/optimal_gc_prob.txt`.

Ensure your Python script handles the calculations accurately and writes only the 4-decimal-place float (e.g., `0.4567`) to the output file.