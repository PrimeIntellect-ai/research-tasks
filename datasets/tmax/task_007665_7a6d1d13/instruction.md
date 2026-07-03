You are an ML engineer preparing training data from protein sequences. You need to extract a specific numerical feature from a FASTA file containing protein sequences by simulating a spectroscopy signal and computing its entropy.

You have a FASTA file located at `/home/user/input.fasta`.

Please write a Python script that processes this file and calculates the features as follows:
1. Parse the FASTA file to extract sequence IDs and their corresponding amino acid sequences.
2. For each sequence, generate a synthetic, unnormalized spectrum represented by a 1D numpy array of length 1000, initialized to zeros.
3. Iterate through each amino acid in the sequence. For an amino acid at index `i` (0-indexed) with character `aa`, compute the frequency bin as: `freq = (ord(aa) * 7) % 1000`. Add the value `(i + 1) * 0.5` to the spectrum array at this `freq` index.
4. Convert this unnormalized spectrum into a probability distribution using the **softmax** function. *Note: Some sequences are very long, which will cause naive exponential calculations to overflow. You must implement a numerically stable softmax.*
5. Smooth the resulting probability distribution using a simple moving average filter of window size 5. Use `numpy.convolve` with the window `np.ones(5)/5.0` and `mode='same'`.
6. Calculate the Shannon entropy of the smoothed signal: `-sum(p * log(p))`. To prevent mathematical errors from zero values, clip the smoothed signal to a minimum of `1e-12` before taking the logarithm.
7. Save the output to a CSV file at `/home/user/features.csv` with exactly two columns: `ID` and `Entropy`.
8. The rows in the CSV must be sorted alphabetically by the sequence `ID`.
9. The `Entropy` values must be rounded to exactly 4 decimal places.

Write and execute the script to generate `/home/user/features.csv`. Ensure your environment has any required libraries installed.