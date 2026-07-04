You are given a stripped binary `/app/score_oracle`. This binary is used as part of a large-scale data storage management pipeline to evaluate and route text documents. It takes a single text file path as an argument and outputs a regression score (float) based on the text contents.

We have lost the original source code for this oracle, but we know the following:
1. It relies on a simple tokenization and word-counting strategy. It reads the text, removes standard punctuation (`.,!?`), converts everything to lowercase, and counts the occurrences of exactly four specific animal names (as whole words).
2. It computes a linear regression score based on the counts of these four words, plus a bias term.

Your task is to:
1. Probe or reverse-engineer `/app/score_oracle` to discover the 4 animal names and their exact linear regression weights (including the base bias/intercept).
2. Write a pure Bash shell script `/home/user/score.sh` (using standard CLI tools like `awk`, `grep`, `sed`, `tr`, `bc`) that accurately recreates this scoring model. 
3. Your script must take a file path as its first argument, perform the same tokenization (lowercase, remove `.,!?`, split by whitespace), count the specific words, and compute the final score.
4. The output of `/home/user/score.sh` must be strictly the numerical score (e.g., `3.50`), with no other text.

Ensure your script is efficient and robust against varying text formats. We will evaluate your script's Mean Squared Error (MSE) against the original oracle on a hold-out dataset of new text files.