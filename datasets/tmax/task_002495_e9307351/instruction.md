You are a bioinformatics analyst tasked with identifying specific k-mer motifs in raw nanopore sequencing current signals. 

We have provided a raw current signal in `/app/raw_signal.txt` (one float value per line, representing picoamperes). We also have a scanned snippet from an instrument manual at `/app/motif_spec.png` which describes the expected statistical distribution of our target k-mer motif.

Your task is to:
1. Extract the target probability distribution parameters (Means and Standard Deviations for a two-state mixture) from the provided image `/app/motif_spec.png`.
2. Segment the raw 1D signal into overlapping windows of size 100 with a step size of 10.
3. Construct a matrix from these windows and apply Truncated Singular Value Decomposition (SVD) to denoise the signals. You must keep only the top 3 singular values to reconstruct the smoothed signals. Ensure your decomposition handles numerical stability by mean-centering each window prior to SVD.
4. For each smoothed window, calculate the 1-Wasserstein distance between the window's empirical empirical distribution and the theoretical Gaussian mixture distribution extracted from the image. 
5. Identify all windows where the Wasserstein distance is strictly less than the threshold specified in the image.
6. Write the original starting indices (0-indexed line numbers from `raw_signal.txt`) of these matching windows to `/home/user/motif_matches.csv`, one integer index per line, sorted in ascending order.

The automated verification will evaluate the F1-score of your detected motif indices against the ground truth. Your algorithm's output must achieve an F1-score of at least 0.85. You may use any programming language you prefer to implement this pipeline.