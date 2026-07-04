You are an analyst tasked with processing an old, corrupted dataset of system event sequences. The data dictionary detailing the tokenization mapping was lost, but a scanned image of it survives. 

Your goal is to build a C-based analysis pipeline that extracts the token mapping, processes the raw event sequences, builds a basic statistical language model, and evaluates a test set.

Here are the specific steps you must complete:

1. **Tokenization Recovery**: 
   An image of the token mapping table is located at `/app/mapping.png`. Use OCR tools (like `tesseract`, which is installed) to extract the mapping. The table maps single alphabetic characters (Event Codes) to integer Token IDs (1 through 5).

2. **Data Preparation**:
   You have two CSV files: `/app/events.csv` (training data) and `/app/test_events.csv` (test data). 
   Each CSV has the format `id,event_sequence`, where `event_sequence` is a space-separated string of Event Codes (e.g., `A C E B`).

3. **C Implementation**:
   Write a C program (e.g., `/home/user/analyze.c`) and compile it. Your program must:
   * Read the recovered token mappings.
   * Parse and tokenize the event sequences from `/app/events.csv`.
   * **Bootstrap Sampling**: Implement a routine to generate 10,000 bootstrap samples (sample rows with replacement) of the training dataset. Calculate the mean token length of the sequences across all 10,000 bootstrap samples.
   * **Model Architecture Reconstruction**: Build a Bigram Language Model from the *original* (non-bootstrapped) training dataset `/app/events.csv`.
     * Calculate bigram probabilities $P(w_i | w_{i-1})$.
     * Assume a universal Start Token (`<s>`) precedes every sequence. Do *not* use an End Token.
     * Use Add-1 (Laplace) smoothing for all bigram counts. The vocabulary size $V$ for smoothing should be exactly 5 (the 5 event codes). 
     * Formula: $P(w_i | w_{i-1}) = \frac{Count(w_{i-1}, w_i) + 1}{Count(w_{i-1}) + 5}$
   * **Inference / Evaluation**: Process `/app/test_events.csv` using your Bigram model. Calculate the overall Perplexity of the test set. 
     * Calculate the base-2 log probability of each sequence: $\sum \log_2 P(w_i | w_{i-1})$
     * Sum the log probabilities across all sequences in the test set.
     * Calculate Perplexity: $2^{- (\text{Total Log Prob} / \text{Total Test Tokens}) }$
     * Total Test Tokens is the total number of actual event codes in the test set (do not count the Start Tokens).

4. **Output Formulation**:
   Your C program should output a final file `/home/user/metrics.txt` containing exactly two lines:
   ```
   Bootstrap_Mean_Length: <value rounded to 4 decimal places>
   Test_Perplexity: <value rounded to 4 decimal places>
   ```

A verification script will read `/home/user/metrics.txt` and check if your `Test_Perplexity` is within an absolute error of `0.05` compared to the exact mathematical value. Ensure your C code logic closely follows the formulas provided!