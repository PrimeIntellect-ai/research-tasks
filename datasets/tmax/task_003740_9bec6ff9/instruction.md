I am a data scientist trying to fit a biophysical model to design a DNA primer using an MCMC sampler. I wrote a C program that finds the optimal 8-mer primer for a target DNA sequence by proposing mutations and accepting them based on a spectral energy score. 

However, I'm encountering a severe reproducibility issue: the spectral energy score is calculated by numerically integrating an array of thousands of `float` values. Because of standard single-precision floating-point accumulation errors, evaluating the array in different permutations (which happens during different alignment proposals in the MCMC) yields slightly different results. This breaks the detailed balance of my MCMC sampler!

I have placed the source code at `/home/user/mcmc_primer.c` and the target DNA sequence at `/home/user/target.txt`.

Your tasks are:
1. Fix the floating-point reduction issue in `/home/user/mcmc_primer.c`. Specifically, modify the `integrate_spectral_energy` function to use the **Kahan summation algorithm**. Do not change the function signature, just the internal loop to use Kahan summation for precise float accumulation.
2. Compile the fixed C program. It requires the math library (`-lm`).
3. Run the compiled program with the arguments: `./mcmc_primer /home/user/target.txt 42` (where 42 is the random seed).
4. The program will print the best primer sequence and its score. Save the exact standard output of this run to `/home/user/result.log`.

The output in `/home/user/result.log` should look exactly like:
```
Best Primer: [8-character string]
Score: [float value]
```