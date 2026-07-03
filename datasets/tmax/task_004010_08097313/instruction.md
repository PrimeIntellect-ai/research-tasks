You are a data scientist working on a reproducible computational pipeline for primer sequence analysis. We have an old compiled binary oracle that calculates a probability distribution distance metric for candidate primer sequences under noisy conditions using a Monte Carlo simulation. We need to replace this binary with a transparent, reproducible Python script.

We have lost the original source code, but we know the exact algorithmic steps. Additionally, the specific motif and reference distribution parameters were left in a colleague's audio note, located at `/app/voicemail.wav`.

Your task is to listen to the audio file to extract the missing parameters, and then write a Python script at `/home/user/primer_model.py` that perfectly replicates the oracle's behavior. 

**Algorithmic Specification for `primer_model.py`:**
1. The script must read a single DNA sequence (a string of A, C, G, T) from standard input (`stdin`).
2. Initialize the built-in Python `random` module by setting the seed to the integer length of the input sequence: `random.seed(len(sequence))`
3. **Monte Carlo Simulation:** Generate 1000 independent mutated versions of the sequence. For each version, iterate through the original sequence character by character. For each character, draw a random float using `random.random()`. If the float is strictly less than 0.05, replace the character with `'A'`; otherwise, keep the original character. (Generate the mutated sequences one by one, character by character in a nested loop).
4. **Sequence Alignment / Motif Scoring:** For each of the 1000 mutated sequences, count the number of non-overlapping occurrences of the target motif (which you must transcribe from `/app/voicemail.wav`). This count is the sequence's score. Store the 1000 scores in a list.
5. **Reference Dataset:** Immediately after computing all 1000 mutation scores, generate a reference dataset of 1000 integers using `[random.randint(MIN_VAL, MAX_VAL) for _ in range(1000)]`. The `MIN_VAL` and `MAX_VAL` are specified in the voicemail.
6. **Probability Distribution Distance:** Calculate the 1D Wasserstein distance between your 1000 Monte Carlo scores and the 1000 reference dataset integers. Use `scipy.stats.wasserstein_distance`.
7. **Output:** Print the Wasserstein distance to `stdout`, formatted to exactly four decimal places (e.g., `1.2345`).

The automated test suite will run your script against thousands of random DNA sequences and compare its output bit-for-bit against our reference oracle. It is critical that your random calls and mathematical operations follow this exact sequence to ensure perfectly reproducible equivalence.