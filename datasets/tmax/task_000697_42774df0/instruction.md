You are a Machine Learning Engineer tasked with preparing and filtering a training dataset entirely in the Linux terminal. You need to identify whether sentences in a new target dataset belong to a specific "target domain" or a "generic domain" using a Naive Bayes-based unigram language model. Because this is a minimal-dependency environment, you must implement the tokenization, probabilistic modeling, and numerical scoring using **only Bash and standard POSIX/GNU command-line utilities** (like `awk`, `sed`, `tr`, `grep`, `sort`, `uniq`, etc.). Do not use Python, Perl, or any other high-level scripting language.

Your objective is to write a main script `/home/user/filter_dataset.sh` that takes three files as input:
1. `domain.txt` (The target domain training corpus)
2. `generic.txt` (The generic domain training corpus)
3. `target.txt` (The new sentences to classify)

**Phase 1: Tokenization & Dataset Preparation**
Implement tokenization for all three files with the following strict rules:
- Convert all text to lowercase.
- Replace any character that is not an English letter (`a-z`) with a single space.
- Condense multiple spaces into a single space, and strip leading/trailing spaces.
- A "word" is any continuous sequence of `a-z` characters.

**Phase 2: Bayesian Inference and Probabilistic Modeling**
Using the tokenized training datasets (`domain.txt` and `generic.txt`), build a unigram language model to classify the sentences in `target.txt`.
- Calculate the total number of words in `domain.txt` ($N_{domain}$) and `generic.txt` ($N_{generic}$).
- Calculate the total Vocabulary size ($V$), which is the number of **unique** words found across *both* training corpora combined.
- For each word $w$, calculate the log-probability for each class using Laplace (Add-1) smoothing:
  $\log P(w | domain) = \ln\left(\frac{\text{count}(w, domain) + 1}{N_{domain} + V}\right)$
  $\log P(w | generic) = \ln\left(\frac{\text{count}(w, generic) + 1}{N_{generic} + V}\right)$
  *Note: Use the natural logarithm (`log()` in awk). If a word in `target.txt` never appeared in the training corpora, its count is 0.*

For each line in `target.txt` (processed line by line), compute the log-likelihood ratio:
$\text{Score} = \sum_{w \in \text{line}} \log P(w | domain) - \sum_{w \in \text{line}} \log P(w | generic)$
Assume equal prior probabilities ($P(domain) = P(generic)$), so they cancel out. 
If Score > 0, classify as `DOMAIN`, otherwise `GENERIC`.

**Phase 3: Output and Numerical Accuracy**
Your script `/home/user/filter_dataset.sh` must process `target.txt` and generate a file exactly at `/home/user/scores.tsv` with the following tab-separated format:
`LINE_NUMBER    SCORE    CLASSIFICATION`
- `LINE_NUMBER`: The 1-based line number from `target.txt` (e.g., 1, 2, 3...)
- `SCORE`: The computed score formatted to exactly 4 decimal places (e.g., `0.1234`, `-1.5000`).
- `CLASSIFICATION`: Either `DOMAIN` or `GENERIC`.

**Execution:**
Ensure your script is executable (`chmod +x /home/user/filter_dataset.sh`). 
When we test your solution, we will run:
`./filter_dataset.sh domain.txt generic.txt target.txt`