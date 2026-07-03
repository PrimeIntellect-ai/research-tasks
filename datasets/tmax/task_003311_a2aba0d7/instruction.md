A fellow researcher is organizing a large collection of dataset files containing numeric vector embeddings, but some of the files have been corrupted with anomalous data (e.g., inconsistent dimensions, or vectors that are wildly out of distribution when calculating cosine similarity against a baseline). 

I need your help setting up our environment and building a robust filtering script in Bash.

First, we are using a vendored data-science utility package for Bash located at `/app/bash-ds-utils`. However, it seems to have a deliberate perturbation—its `Makefile` has a hardcoded incorrect path that prevents it from compiling its helper C binary (used for fast experiment tracking logging), and a script `setup_env.sh` contains a wrong environment variable `TRACKER_HOME`. 
1. Fix the perturbation in `/app/bash-ds-utils` so that `make install` succeeds and the known-good code path (`/app/bash-ds-utils/bin/track_exp --init`) runs without errors.

Second, I need you to create a classification script at `/home/user/filter.sh`. 
This script must take a single file path as its argument and exit with code `0` if the dataset is "clean" (valid), and exit with code `1` if it is "evil" (corrupted/anomalous).
The datasets are TSV files where each line is a vector. 
To determine if a dataset is clean, your script should use core utilities (like `awk`, `shuf`, etc.) to:
- Verify dimensionality: Every vector in the file must have exactly 50 dimensions.
- Sample and measure similarity: Randomly sample (with replacement, bootstrap style) 100 rows from the dataset. Calculate the Euclidean distance of each sampled row against a baseline vector of all `0.1`s. If the average distance of the sample is greater than 15.0 or less than 5.0, reject the file.
- Track the experiment: Call the fixed `/app/bash-ds-utils/bin/track_exp --log <filename> --status <clean|evil>` for each evaluated file.

There are test corpora available:
- Clean corpus: `/home/user/data/clean/`
- Evil corpus: `/home/user/data/evil/`

Your script must perfectly preserve all files in the clean corpus (exit 0) and reject all files in the evil corpus (exit 1).