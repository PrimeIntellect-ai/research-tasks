I am a bioinformatics researcher running simulations on genomic data, and I need your help building a sequence filtering pipeline. 

We have a proprietary, closed-source feature extractor binary located at `/app/extract_signal`. When you run `/app/extract_signal <path_to_fasta>`, it outputs a time-series signal (a list of floating-point numbers, one per line) corresponding to the structural properties of the sequence.

Unfortunately, some of our sequences contain experimental artifacts that manifest as high-frequency periodic noise in the extracted signal. I need a Bash script `/home/user/filter.sh` that acts as a classifier/filter to separate the clean sequences from the anomalous ("evil") ones.

Your script must:
1. Accept two arguments: an input directory containing `.fasta` files, and an output directory where clean files should be copied. Usage: `/home/user/filter.sh <input_dir> <output_dir>`
2. Process the files in parallel using `xargs -P` or `GNU parallel` to speed up the workflow.
3. For each file, run the `/app/extract_signal` binary to get the signal.
4. Perform a spectral analysis (Fourier transform) on the signal to compute the energy in the high-frequency band (defined here as frequencies $f > 0.25$ cycles/sample). You may use Python (e.g., `numpy`) inline or as a helper script to compute the FFT.
5. Use a bootstrap resampling method (at least 1000 iterations) to estimate the 95% confidence interval of the mean high-frequency energy across the signal windows.
6. If the bootstrap lower bound of the high-frequency energy indicates the presence of the periodic artifact, the script should REJECT the file (do not copy it). Otherwise, it must ACCEPT the file by copying it to the `<output_dir>`.

To help you develop and test your script, I have provided two datasets:
- `/app/corpus/clean/`: Contains known clean FASTA files. Your script MUST preserve (copy) 100% of these.
- `/app/corpus/evil/`: Contains known anomalous FASTA files. Your script MUST reject (ignore) 100% of these.

Write the `/home/user/filter.sh` script so that it correctly classifies the provided corpora. Ensure it is executable.