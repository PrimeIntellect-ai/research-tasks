You are a Machine Learning Engineer tasked with building a lightweight, Bash-only data preparation and evaluation pipeline for a probabilistic language model. 

Your goal is to implement a bigram language model using Add-One (Laplace) smoothing, entirely through Bash scripts and standard POSIX/GNU utilities (like `awk`, `sed`, `grep`, `bc`, etc.). Do not use Python, Perl, or any other scripting languages.

**Phase 1: Tokenization and Model Building**
Create a script at `/home/user/build_model.sh` that performs the following:
1. Reads the raw text file located at `/home/user/corpus.txt`.
2. Normalizes the text: converts all characters to lowercase and removes all non-alphabetic characters (replace them with spaces).
3. Tokenizes the text into unigrams and bigrams.
4. Calculates the vocabulary size $V$ (the number of unique unigrams in the entire corpus).
5. Computes the Add-One smoothed probability for every bigram that actually appears in the corpus. The formula is:
   $P(w_2 | w_1) = \frac{C(w_1, w_2) + 1}{C(w_1) + V}$
   where $C(x)$ is the count of occurrences in the corpus.
6. Saves these probabilities to `/home/user/model.tsv`. The file must be tab-separated with columns: `word1`, `word2`, `probability`. The probability must be formatted to exactly 4 decimal places (e.g., `0.2500`). Sort the file alphabetically by `word1` then `word2`.

**Phase 2: Inference Benchmarking**
Create a script at `/home/user/benchmark.sh` that performs the following:
1. Reads a test file located at `/home/user/test.txt` (one sentence per line).
2. For each line, normalizes and tokenizes it exactly as in Phase 1.
3. Computes the log probability of the sentence. The log probability is the sum of the natural logarithms ($\ln$) of its bigram probabilities.
   - If a bigram from the test sentence appeared in the training corpus, use its probability from `model.tsv`.
   - If a bigram did *not* appear in the training corpus, but $w_1$ did, its smoothed probability is $\frac{1}{C(w_1) + V}$.
   - If $w_1$ never appeared in the training corpus (completely unknown word), its smoothed probability for any following word is $\frac{1}{V}$.
4. Writes the results to `/home/user/scores.tsv` in the format: `LineNumber \t LogProb` (Line numbers start at 1, format log probability to 4 decimal places).
5. Uses the `time` command (or `date`) to measure the execution time of the scoring process and writes the timing output to `/home/user/time.log`.

Execute both scripts to generate `/home/user/model.tsv`, `/home/user/scores.tsv`, and `/home/user/time.log`. Ensure your scripts are executable.