You are a performance engineer profiling a bioinformatics Monte Carlo simulation pipeline. 

A researcher has written a Bash script at `/home/user/slow_mcmc.sh` that performs a 1D Random Walk (a simple MCMC-like sampling) based on the GC content of a DNA sequence in `/home/user/seq.fasta`. It reads pre-generated random integers from `/home/user/randoms.txt` to ensure reproducible simulations.

However, the script is incredibly slow and takes minutes to process 50,000 steps. Profiling reveals this is because it spawns the `bc` utility inside a loop for every single step. Furthermore, using floating-point division can introduce subtle numerical stability and precision issues.

Your task is to write an optimized version of this script at `/home/user/fast_mcmc.sh`.
Your optimized script must:
1. Be written in Bash.
2. Read the sequence from `/home/user/seq.fasta` and calculate its length ($L$) and total count of 'G' and 'C' characters ($GC$).
3. Read the random integers from `/home/user/randoms.txt`.
4. Iterate over the random integers ($R$). For each integer:
   - Step $X$ up by 1 if $R / 32767 < GC / L$.
   - Step $X$ down by 1 otherwise.
   - Start with $X=0$.
5. **Crucially**, you must avoid floating-point math entirely in the loop to fix numerical stability issues and eliminate the need for `bc`. Use pure Bash integer arithmetic (hint: cross-multiplication) to evaluate the inequality exactly.
6. Print the final value of $X$ to standard output.

Once you have written `/home/user/fast_mcmc.sh`, make it executable and run it. Redirect its final output to `/home/user/result.txt`.

Ensure your script completes in just a few seconds. Do not use external tools like `bc`, `awk`, or `python` inside the main loop.