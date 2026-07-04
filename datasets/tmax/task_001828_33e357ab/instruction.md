You are a data scientist preparing a massive text dataset for a language model. You need to clean the raw data by removing toxic and anomalous documents. To do this, you will use a local Bayesian text classification utility, but the provided utility is currently broken.

Your objectives are:

1. **Fix the Vendored Package**: 
   You have been provided with the source code for `bayes_text_filter` located at `/app/bayes_text_filter-1.2.0/`.
   - This package is supposed to compile a small C binary and provide a Bash wrapper `bayes_score.sh` to evaluate text files. 
   - However, the `Makefile` and the wrapper script contain deliberate errors preventing compilation and execution. 
   - Fix the package so that running `make` succeeds and `./bayes_score.sh <file>` outputs a numerical spam/anomaly score. (A score > 50 indicates an anomalous document).

2. **Create a Dataset Cleaner**:
   - Write a Bash script at `/home/user/clean_dataset.sh`.
   - The script must accept exactly two arguments: an input directory containing text files and an output directory. 
     Usage: `/home/user/clean_dataset.sh <input_dir> <output_dir>`
   - The script should iterate through all `.txt` files in the `<input_dir>`.
   - It must tokenize the text (convert to lowercase, remove punctuation) and feed it to the fixed `/app/bayes_text_filter-1.2.0/bayes_score.sh`.
   - If the document scores 50 or less, copy it to the `<output_dir>` with the same filename. If it scores higher than 50, discard it.
   - For any file processed, append a log entry to `/home/user/cleaning.log` in the format: `[KEEP|DROP] filename score`

Your solution must be robust against our hidden test suites containing clean text (which must be preserved) and malicious/toxic text (which must be rejected). Do not use the internet or attempt to install external packages.