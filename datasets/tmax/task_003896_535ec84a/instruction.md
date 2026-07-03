You are acting as a machine learning engineer preparing a synthetic training dataset for a model that predicts primer binding efficiency. 

You need to write a Bash script `/home/user/prepare_data.sh` that orchestrates a Monte Carlo simulation to generate random primers, compiles a fast C-based alignment tool from source, and creates a regression dataset.

Here are the requirements for your script:
1. **Compilation**: Create a directory `/home/user/bin`. Compile the provided C source file `/home/user/src/scoring.c` into an executable named `/home/user/bin/score_ext` using `gcc` with standard optimizations (`-O2`).
2. **Primer Generation (Monte Carlo)**: Generate exactly 100 random DNA sequences (primers) of length 12. To ensure reproducible training data, use Python inline within your Bash script to generate these primers with the following specification: Use the `random` module, set `random.seed(123)`, and generate each primer by randomly choosing characters from the string `'ACGT'` 12 times.
3. **Sequence Alignment Scoring**: Read the target DNA sequence from the file `/home/user/target.txt`. Loop through your 100 generated primers, and for each primer, execute the compiled `/home/user/bin/score_ext` passing the primer as the first argument and the target sequence as the second argument. The C program will output an integer alignment score.
4. **Output formatting**: Your Bash script must save the results to `/home/user/dataset.csv`. The file must contain exactly 100 lines, formatted as `<primer_sequence>,<score>` (e.g., `ATGCATGCATGC,5`). Do not include a header row.

Make sure your script is executable and run it to produce the final `dataset.csv`.