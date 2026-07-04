You are a bioinformatics analyst studying the spatial distribution of a specific Transcription Factor Binding Site (TFBS) across a newly sequenced genomic region. 

You have been provided with a file at `/home/user/tfbs_positions.txt` containing the integer coordinates of all identified TFBS occurrences on the chromosome (one coordinate per line).

Your goal is to model the density of these binding sites and find a specific boundary coordinate using numerical methods in Python.

Perform the following steps:
1. Load the TFBS coordinates from `/home/user/tfbs_positions.txt`.
2. Fit a Gaussian Kernel Density Estimate (KDE) to these coordinate positions. You must use `scipy.stats.gaussian_kde` with its default bandwidth estimator (Scott's rule).
3. We need to identify the exact spatial coordinate $X$ that bounds the lower 90% of the binding site density. Formally, you must find the root $X$ such that the integral of the KDE from $-\infty$ to $X$ is exactly $0.90$:
   $$ \int_{-\infty}^{X} \text{KDE}(x) dx = 0.90 $$
4. Use a nonlinear equation solving method (e.g., from `scipy.optimize`) and numerical integration to find $X$. You can assume the root lies somewhere between $0$ and $150000$.
5. Round your calculated coordinate $X$ to exactly 2 decimal places.
6. Write only this rounded numerical value to a file located at `/home/user/percentile_90.txt`.

Ensure your final script runs cleanly and produces the correct output file.