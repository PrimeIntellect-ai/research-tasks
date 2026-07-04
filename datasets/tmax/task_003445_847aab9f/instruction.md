You are a performance engineer working on a bioinformatics pipeline. Your team uses a C program to simulate spectroscopic sensor signals by analyzing the distance distribution between Alpha-Carbon ('CA') atoms in protein structures (PDB format). 

The previous implementation was accidentally deleted during a server migration, and you need to rewrite it optimally in C.

**Task Requirements:**
1. Write a C program at `/home/user/spectro_profile.c`.
2. The program must read a standard PDB file located at `/home/user/input.pdb`.
3. Parse the file to extract the 3D coordinates (x, y, z) of all atoms where the atom name is exactly `CA` (Alpha-Carbon). Note: The PDB ATOM record format specifies the atom name at columns 13-16.
4. Compute the Euclidean distance between all unique pairs of 'CA' atoms (i.e., for $N$ CA atoms, there are $N(N-1)/2$ unique pairs).
5. Estimate the probability density distribution of these distances using a 1D histogram:
   - The histogram must have exactly 100 bins.
   - The range is $[0, 100)$ Ångstroms (bin 0 is $[0, 1)$, bin 1 is $[1, 2)$, ..., bin 99 is $[99, 100)$).
   - Normalize the histogram by the total number of pairs to create a probability distribution $P$. (If a distance is $\ge 100$, ignore it for the total count).
6. Calculate the Kullback-Leibler (KL) divergence of $P$ relative to a uniform reference distribution $Q$, where $Q(i) = 1/100 = 0.01$ for all bins.
   - The KL divergence formula is: $D_{KL}(P || Q) = \sum P(i) \ln\left(\frac{P(i)}{Q(i)}\right)$
   - Only include bins where $P(i) > 0$. Use the natural logarithm (`log()` in C).
7. The program must write *only* the final KL divergence value to `/home/user/kl_divergence.txt`, formatted to exactly 6 decimal places (e.g., `1.234567`).

**Execution:**
Compile your code using `gcc -O3 -lm spectro_profile.c -o spectro_profile`.
Run the compiled binary. Ensure the output file `/home/user/kl_divergence.txt` is successfully created with the correct value.