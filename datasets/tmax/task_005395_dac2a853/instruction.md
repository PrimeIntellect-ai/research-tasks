You are a data scientist fitting a simple mixture model to represent a target microbial community. 

You have a FASTA file located at `/home/user/community.fasta` containing three sequences:
- `Target`: The combined genetic profile of the target community.
- `Source1`: The genetic profile of the first source organism.
- `Source2`: The genetic profile of the second source organism.

Your goal is to find the optimal mixing weight of `Source1` and `Source2` that best approximates the `Target` profile based on single-nucleotide frequencies.

Please write and execute a Python script at `/home/user/fit_mixture.py` that performs the following steps:
1. Parses the FASTA file `/home/user/community.fasta`.
2. Computes the probability distribution of 1-mers (the relative frequencies of the single nucleotides A, C, G, and T) for each of the three sequences. Ensure the frequency vectors are consistently ordered (e.g., alphabetical: A, C, G, T).
3. Uses an optimization routine (e.g., `scipy.optimize.minimize`) to find the mixing weight $w$ (where $0 \le w \le 1$) such that the mixture distribution $P_{mix} = w \cdot P_{Source1} + (1 - w) \cdot P_{Source2}$ minimizes the Sum of Squared Errors (SSE) compared to the $P_{Target}$ distribution.
4. Writes the optimal mixing weight $w$ to a log file at `/home/user/optimal_weight.txt`. The value should be rounded to exactly 3 decimal places (e.g., `0.123`).

After writing the script, execute it to ensure `/home/user/optimal_weight.txt` is generated with the correct format. You only have access to standard Python scientific libraries (like `scipy`, `numpy`) and standard Linux CLI tools. Do not install external bioinformatics parsing libraries like `Biopython`; parse the FASTA file using standard Python.