You are a Machine Learning Engineer preparing a dataset for a model that classifies raw acoustic/electrical signals of DNA (similar to nanopore sequencing). 

You have been given a combined data file located at `/home/user/data.txt`. 
The file has exactly two lines:
1. A basecalled DNA sequence (a string of A, C, G, T).
2. A comma-separated list of float values representing the raw experimental signal. There are exactly 10 signal samples for every 1 base in the DNA sequence.

Your task is to write a C++ program (`/home/user/extract_features.cpp`) to extract frequency-domain features for the biological payload, filtering out the synthetic adapter/primer.

Specifically, your C++ program must:
1. Read `/home/user/data.txt`.
2. Perform a basic sequence alignment/search to find the exact first occurrence of the primer sequence: `ATGCGAT`.
3. Identify the start of the "payload" sequence, which begins immediately after the primer ends.
4. Extract exactly **50 signal samples** corresponding to the first 5 bases of the payload (since there are 10 samples per base, if the payload starts at character index `P`, the signal starts at float index `10 * P`).
5. Compute the Discrete Fourier Transform (DFT) of these 50 time-domain samples. 
   The DFT $X_k$ for a signal $x_n$ of length $N=50$ is defined as:
   $X_k = \sum_{n=0}^{N-1} x_n e^{-i 2 \pi k n / N}$
6. Calculate the magnitude of each frequency bin $k$ from $0$ to $49$. ($\text{Magnitude} = \sqrt{\text{Re}(X_k)^2 + \text{Im}(X_k)^2}$)
7. Output the results to a CSV file at `/home/user/features.csv`. The CSV must have a header `Bin,Magnitude` and contain 50 rows of data. Format the magnitude to exactly 4 decimal places (e.g., `0.0000`).

Compile and run your C++ program so that `/home/user/features.csv` is generated successfully. Do not use external libraries (like FFTW) for the math; write a standard library-only C++ implementation.