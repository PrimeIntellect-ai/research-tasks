You are a data scientist working on modeling the spatial distribution of atomic coordinates in protein structures. You are using domain decomposition to split the protein into smaller spatial regions (meshes) and fitting a Gaussian mixture model. However, your matrix factorization step keeps crashing because some sub-domains contain near-singular covariance matrices (e.g., when atoms are highly co-planar or co-linear). 

Your task is to write a C program that parses a PDB file, splits the domain, calculates the 3x3 population covariance matrix for the coordinates in each domain, tests for singularity using the determinant, and logs the results.

Write a C program at `/home/user/process_pdb.c` that does the following:
1. Accepts a single command-line argument: the path to a PDB file.
2. Parses the file and extracts the X, Y, and Z coordinates from all lines starting with the exact string `ATOM  `.
   - The coordinates in a standard PDB are found at specific columns, but for this task, you can safely assume that the coordinates are the 6th, 7th, and 8th space-separated tokens on the `ATOM` lines.
3. Determine the global minimum and maximum X coordinates ($X_{min}$ and $X_{max}$) across all parsed ATOMs.
4. Calculate the midpoint $X_{mid} = (X_{min} + X_{max}) / 2.0$.
5. Perform a 1D domain decomposition:
   - **Left Domain**: All atoms with $X < X_{mid}$
   - **Right Domain**: All atoms with $X \ge X_{mid}$
6. For each domain (Left, then Right), calculate the 3x3 **population covariance matrix** of the $(X, Y, Z)$ coordinates. 
   - Note: Use population covariance (divide by $N$, not $N-1$).
7. Calculate the determinant of the covariance matrix for both domains.
8. Compare the determinant against a hypothesis threshold. If the determinant is strictly less than `0.1`, flag it as `SINGULAR`, otherwise flag it as `OK`.
9. Append the output to `/home/user/output.txt` in exactly this format:
```
Domain Left: N_atoms=<N>, det=<det_formatted_to_6_decimal_places>, status=<OK|SINGULAR>
Domain Right: N_atoms=<N>, det=<det_formatted_to_6_decimal_places>, status=<OK|SINGULAR>
```

**Constraints:**
- Write the code in standard C (C99 or later).
- Compile your program into `/home/user/process_pdb` using `gcc`.
- Run your program on the provided file `/home/user/input.pdb`.

Example execution:
```bash
gcc /home/user/process_pdb.c -o /home/user/process_pdb -lm
/home/user/process_pdb /home/user/input.pdb
```