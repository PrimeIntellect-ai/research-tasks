You are tasked with assisting a data scientist in analyzing a spectroscopy experiment. The workflow involves processing a video of an interferometer output, and creating a robust, reproducible signal processing pipeline.

Part 1: Video Analysis
We have a recording of the experiment at `/app/spectroscopy.mp4`.
1. Extract the frames of this video.
2. Calculate the total sum of grayscale pixel intensities for each frame.
3. Find the 0-based index of the frame with the highest total intensity.
4. Write this integer index to `/home/user/peak_frame.txt`.

Part 2: Signal Analyzer
We need to fit a model to the spectral data and calculate confidence intervals. Since our pipeline handles diverse data streams, you must write a standalone executable tool located at `/home/user/signal_analyzer`. You may write this in any language you prefer (Python, C++, etc.), but it must be executable directly (e.g., via a shebang like `#!/usr/bin/env python3` and `chmod +x`, or compiled to a binary).

Tool Specifications:
- **Input:** Reads a single line from standard input containing a comma-separated list of float values (the signal). The length will be between 10 and 100 values.
- **Processing:** 
  1. Apply a moving average filter of window size 3. (For an input array $X$ of length $N$, the smoothed array $S$ will have length $N-2$, where $S_i = (X_i + X_{i+1} + X_{i+2}) / 3$).
  2. Perform a bootstrap analysis on the smoothed array $S$ to find the 95% confidence interval of the mean.
  3. Use exactly 1000 bootstrap resamples.
  4. Use the percentile method (2.5th and 97.5th percentiles).
  5. For reproducibility, initialize your random number generator with the seed `42` before generating the resamples. (If using Python, use `numpy.random.seed(42)` and `numpy.random.choice`).
- **Output:** Print the confidence interval to standard output in exactly this format, rounded to 4 decimal places:
  `CI: [lower, upper]`

Example:
If the smoothed data has a mean of 1.23456, you might output:
`CI: [1.1023, 1.3501]`

An automated verifier will randomly generate hundreds of input sequences and assert that your `/home/user/signal_analyzer` matches our reference oracle bit-for-bit.