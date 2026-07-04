You are a bioinformatics analyst working on Genomic Signal Processing (GSP). We are trying to identify coding regions in DNA by detecting the well-known "period-3" property (a peak in the Fourier spectrum at frequency f = 1/3). 

To do this, we map the nucleotide characters (A, C, G, T) to numerical values. However, the optimal numerical mapping that maximizes the signal-to-noise ratio of the period-3 peak is unknown.

You need to write a Bash orchestration script that finds the optimal integer mapping. 

Here is what you need to do:
1. Install `papermill`, `jupyter`, `numpy`, and `scipy` using pip.
2. We have a pre-existing Jupyter notebook at `/home/user/calc_fft.ipynb` (which you must assume is already created for you in the environment). This notebook is parameterized with 4 variables: `valA`, `valC`, `valG`, and `valT`. It reads a DNA sequence from `/home/user/sequence.txt`, converts it to a numerical sequence using those parameters, computes the Fast Fourier Transform (FFT), calculates the signal-to-noise ratio at the N/3 frequency, and writes the resulting floating-point score to `/home/user/current_score.txt`.
3. Write a Bash script at `/home/user/optimize.sh`. This script must perform a Grid Search over all 24 permutations of the values {1, 2, 3, 4} assigned to (valA, valC, valG, valT). 
4. For each permutation, your Bash script should use `papermill` to execute `/home/user/calc_fft.ipynb` (save the output notebook to `/tmp/out.ipynb`), passing the current values of `valA`, `valC`, `valG`, and `valT` as parameters.
5. After running `papermill`, read the score from `/home/user/current_score.txt`.
6. Your script must keep track of the permutation that yields the highest score.
7. Finally, your script should write the best mapping and its score to `/home/user/best_mapping.csv` in exactly this format: `valA,valC,valG,valT,score`.

Ensure your Bash script is executable and run it to produce the final `best_mapping.csv` file. 
Do not modify the `calc_fft.ipynb` notebook. Rely entirely on your Bash script to orchestrate the notebook evaluations and optimization logic.