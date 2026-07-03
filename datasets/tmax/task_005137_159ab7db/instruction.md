You are a data scientist tasked with cleaning a noisy dataset of text using Bayesian inference and evaluating the cleaning process using bootstrap sampling.

Your workspace contains two files in `/home/user/`:
1. `raw_texts.txt`: Contains noisy text sentences, one per line.
2. `word_priors.csv`: A CSV containing valid words and their prior probabilities (`word,prior`).

Your goals are to:
1. **Tokenize and Clean the Dataset**:
   - Tokenize each line in `raw_texts.txt` by splitting on whitespace.
   - For every token (let's call it the "noisy token" $t_n$), find the most likely original valid word $w$ from `word_priors.csv` using Maximum A Posteriori (MAP) estimation.
   - The posterior probability is proportional to the likelihood times the prior: $P(w | t_n) \propto P(t_n | w) \times P(w)$
   - Use the following likelihood model based on Levenshtein distance: 
     $P(t_n | w) = 0.1^{\text{Levenshtein}(t_n, w)}$
   - For each $t_n$, select the word $w$ from the CSV that maximizes $P(t_n | w) \times P(w)$. If there is a tie for the maximum probability, resolve it by picking the word that comes first alphabetically.
   - Save the cleaned text (sentences reconstructed with space-separated cleaned words) to `/home/user/cleaned_texts.txt`.

2. **Statistical Evaluation**:
   - For each sentence, calculate the "replacement fraction": the number of tokens that were changed (i.e., the MAP estimated word $w$ is not identical to the original noisy token $t_n$) divided by the total number of tokens in that sentence.
   - You will have an array of replacement fractions (one per sentence).
   - Use bootstrap resampling to compute the 95% confidence interval for the **mean** of these replacement fractions.
   - Bootstrap specifications: 10,000 resamples (sampling with replacement from the array of fractions), using the 2.5th and 97.5th percentiles. Use `numpy` with a random seed of `42` (`np.random.seed(42)`) before generating your resamples. The resample size should be equal to the number of sentences.
   - Save the confidence interval to `/home/user/bootstrap_ci.txt` in the exact format: `[lower_bound, upper_bound]` with values rounded to 4 decimal places (e.g., `[0.1234, 0.5678]`).

You may need to install external libraries (e.g., `python-Levenshtein`, `numpy`, `pandas`) using `pip`. Provide scripts to perform these operations and execute them.