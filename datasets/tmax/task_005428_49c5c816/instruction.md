As a machine learning engineer, you are preparing training data for a sequence alignment model. Our downstream matrix factorization model keeps failing on near-singular input matrices, so we need to regularize our sequence distance metrics.

We have an image of a custom nucleotide substitution matrix at `/app/substitution_matrix.png`. 

Your task is to:
1. Extract the 4x4 substitution matrix (for A, C, G, T, in that order) from the image.
2. Write a Python command-line utility at `/home/user/prep_features.py` that accepts exactly two arguments: two DNA sequences of equal length (composed of A, C, G, T).
3. The script must:
   a. Compute the total substitution score between the two sequences by comparing characters at each position and looking up the penalty/reward in the extracted matrix.
   b. Construct a 2x2 matrix `M` where `M[0][0]` is the GC-content (percentage, 0.0 to 1.0) of sequence 1, `M[1][1]` is the GC-content of sequence 2, `M[0][1]` is the proportion of identical matches between the two, and `M[1][0]` is the substitution score divided by the maximum possible score (which is the sequence length times the maximum value in the substitution matrix).
   c. To prevent the near-singular matrix failures we've been seeing in the factorisation, add a regularization term of `0.01` to the diagonal of `M`.
   d. Calculate the determinant of this 2x2 matrix.
   e. Print a single string to standard output in the exact format: `Score: <score>, Det: <determinant rounded to 4 decimal places>`.

Ensure your script handles standard multi-dimensional array manipulation using `numpy` and operates perfectly via the CLI. We will test your script against a large set of random DNA sequence pairs to ensure it matches our internal reference implementation exactly.