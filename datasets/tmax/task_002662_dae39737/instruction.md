You are an assistant helping a researcher run simulations and filter out anomalous experimental data. 

We have a vendored C-based simulation package located at `/app/simkit-1.2/`. 
First, you need to compile this package. The package has a `Makefile`, but it seems to be failing during compilation due to a missing math library linkage. Fix the `Makefile` so that running `make` successfully produces the `/app/simkit-1.2/sim` executable.

Second, the researcher has collected a large dataset of simulation outputs, but some of the sensors drifted, producing "evil" corrupted data alongside the "clean" data. We need an automated filter. 
The datasets are provided in two directories for you to train and test your filter:
- `/app/corpus/clean/` (contains 50 valid simulation runs)
- `/app/corpus/evil/` (contains 50 anomalous simulation runs)

Each file contains 100 rows of floating-point sensor readings. Both clean and evil datasets have approximately the same mean, but the anomalous data has significantly higher variance and occasional extreme outliers due to sensor drift.

Your task is to write a bash script named `/home/user/classifier.sh` that takes a single file path as an argument.
- The script must exit with code `0` if the file is "clean".
- The script must exit with code `1` if the file is "evil" (anomalous).
- To achieve this, your script must use a statistical hypothesis comparison or a bootstrap confidence interval (e.g., checking if the variance or the 95th percentile exceeds a certain threshold). You may use standard CLI tools (`awk`, `sort`, `bc`, `grep`) or a short inline Python/R script within the bash script.

Requirements:
1. Fix the Makefile and compile the `sim` executable in `/app/simkit-1.2/`.
2. Write `/home/user/classifier.sh <file_path>` to correctly classify the files.
3. Your script will be tested against the hidden verification corpora. It must preserve 100% of the clean corpus (exit 0) and reject 100% of the evil corpus (exit 1).

Make sure `/home/user/classifier.sh` is executable.