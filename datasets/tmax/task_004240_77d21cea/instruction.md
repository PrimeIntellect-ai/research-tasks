You are a bioinformatics analyst testing a newly developed C-based sequence profile simulator located at `/home/user/seq_sim.c`. We suspect that aggressive compiler optimizations are changing the floating-point reduction order during the summation of sequence probabilities, leading to non-reproducible distribution results.

Your task is to quantify this effect by doing the following entirely from the command line:

1. Compile the source file `/home/user/seq_sim.c` into two separate executables:
   - `/home/user/seq_strict` using strict, unoptimized settings: `gcc -O0`
   - `/home/user/seq_fast` using aggressive optimizations: `gcc -O3 -ffast-math`

2. Run both executables. Each will output a normalized probability distribution of nucleotides (A, C, G, T) in the format:
   ```
   A: 0.25xxxxxx
   C: 0.24xxxxxx
   ...
   ```

3. Using standard shell tools (like `awk`, `paste`, `bc`, etc.), calculate the absolute difference in the calculated probability for each of the 4 nucleotides between the two runs. 

4. Determine the Maximum Absolute Difference (the Chebyshev distance) between the two probability distributions.

5. Write this single maximum absolute difference value, formatted to exactly 8 decimal places (e.g., `0.00123456`), to the file `/home/user/max_diff.txt`.

Ensure your calculations correctly parse the outputs and that `/home/user/max_diff.txt` contains nothing but the single numeric value.