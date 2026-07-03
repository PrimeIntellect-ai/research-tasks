You are a performance engineer optimizing a bioinformatics data processing pipeline. We have a legacy system that calculates the Gaussian Kernel Density Estimation (KDE) of local GC-content in DNA sequences. 

The current tool is a black-box oracle located at `/app/oracle.py`. It is too slow and we need you to write a clean, optimized Python implementation at `/home/user/fast_kde.py` that produces the exact same bit-for-bit output as the oracle.

Here is what the algorithm is supposed to do:
1. Read a single DNA sequence (containing only A, C, G, T) from standard input (`stdin`).
2. If the sequence length $L$ is less than the window size $W$, print `INVALID` and exit.
3. Calculate the GC-content (fraction of 'G' and 'C' characters) for every overlapping sliding window of size $W$. The windows should step by 1 character (so there are $L - W + 1$ windows in total). Let these values be $gc_1, gc_2, ..., gc_N$.
4. Evaluate an unnormalized Gaussian kernel sum at 5 fixed target points $X = \{0.1, 0.3, 0.5, 0.7, 0.9\}$ using bandwidth $h$.
   Formula for each point $x \in X$:
   $$K(x) = \sum_{i=1}^{N} \exp\left(-\frac{(x - gc_i)^2}{2 h^2}\right)$$
5. Print the 5 resulting values separated by commas, rounded to exactly 4 decimal places (e.g., `0.1234,1.2340,5.6789,0.0000,0.0000`).

The exact parameters for Window Size ($W$) and Bandwidth ($h$) were documented by the original scientist in a screenshot located at `/app/config.png`. You will need to extract these parameters from the image to ensure your script matches the oracle exactly. You may use `tesseract` to read the image.

Write your optimized code in `/home/user/fast_kde.py`. The script must read from `stdin` and print strictly to `stdout`. Automated fuzz-testing will pipe hundreds of random DNA sequences into both your script and the oracle to guarantee 100% equivalence.