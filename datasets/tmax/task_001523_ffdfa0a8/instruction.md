You are assisting a bioinformatics researcher who is running simulations on DNA sequences to extract spectral features. Their current pipeline suffers from non-reproducible results due to floating-point reduction order issues when the input data is decomposed and processed in parallel or varying chunk sizes.

Your task is to build a robust, reproducible Bash pipeline that integrates domain decomposition, FASTA parsing, spectral analysis, and density estimation, while guaranteeing bit-for-bit identical results regardless of the chunking factor.

You need to write a script at `/home/user/pipeline.sh` that takes a single integer argument `<num_chunks>`.

The script must perform the following steps:
1. **Domain Decomposition & Parsing**: Read the FASTA file located at `/home/user/data/input.fasta`. Split the sequences evenly (or as evenly as possible) into `<num_chunks>` temporary files. 
2. **Signal Translation**: For each sequence, translate the DNA characters to numeric signals: A=1.1, C=2.2, G=3.3, T=4.4. Join the numbers with commas.
3. **Spectral Analysis**: For each translated sequence, invoke the pre-existing Python script `/home/user/scripts/fft_power.py --signal "<numeric_string>"`. This script will print a single floating-point number representing the dominant spectral power of the sequence.
4. **Order-Independent Reduction**: Sum all the spectral powers from all sequences. To prevent floating-point reduction order differences, you MUST gather all the individual power values, **sort them numerically**, and sum them using `bc` with a scale of 4.
5. **Density Estimation (Histogram)**: Calculate a simple density histogram of the spectral powers. The bins are defined by integer floors of the powers (e.g., a power of 3.4 falls into bin `3`). Count how many sequences fall into each integer bin.

Your script `/home/user/pipeline.sh` must output exactly this format to standard output:
```
TOTAL_POWER: <summed_value_to_4_decimal_places>
HISTOGRAM:
Bin 0: <count>
Bin 1: <count>
...
Bin N: <count>
```
Only include bins from 0 up to the maximum bin that contains at least one sequence.

Constraints:
- Use `bash` as your primary scripting language.
- Ensure the script is executable.
- Do not modify `/home/user/scripts/fft_power.py` or `/home/user/data/input.fasta`.
- The `TOTAL_POWER` must remain strictly identical whether `pipeline.sh` is called with `1` chunk or `10` chunks.