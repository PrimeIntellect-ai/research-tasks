You are an AI assistant helping a data researcher organize a batch of textual dataset fragments. The researcher wants to categorize these files based on a simple linear algebra scoring model using word frequencies (a basic form of feature selection and dimensionality reduction), and they want it done entirely using Bash utilities.

Here is your task:

1. Look in the directory `/home/user/datasets` (which contains several `.txt` files).
2. **Feature Selection (Dimensionality Reduction):** Find the 5 most globally frequent words across ALL `.txt` files in that directory. 
   - A "word" is strictly defined as a contiguous sequence of alphanumeric characters that is strictly greater than 2 characters long.
   - Convert all text to lowercase before processing.
   - Punctuation should be treated as spaces.
   - If there is a tie in frequencies, sort alphabetically.
3. **Model Architecture & Linear Algebra:** Assign weights to these top 5 words based on their rank: 
   - Rank 1 (most frequent) = weight 5
   - Rank 2 = weight 4
   - Rank 3 = weight 3
   - Rank 4 = weight 2
   - Rank 5 = weight 1
4. **Inference (Scoring):** For each `.txt` file, calculate a "relevance score". The score is the dot product of the file's term frequency vector for the top 5 words and the weight vector. (e.g., if a file has the Rank 1 word 2 times and the Rank 2 word 1 time, and doesn't have the others, its score is `(2 * 5) + (1 * 4) = 14`).
5. **Organization:** 
   - Create directories `/home/user/high_relevance` and `/home/user/low_relevance`.
   - If a file's score is `>= 15`, move it to `/home/user/high_relevance/`.
   - Otherwise, move it to `/home/user/low_relevance/`.
6. **Logging:** Create a log file at `/home/user/scores.log` that lists the original filename (just the basename, e.g., `file1.txt`) and its score, separated by a colon, sorted alphabetically by filename. Example:
   ```
   data_a.txt:24
   data_b.txt:8
   ```

Write a Bash script at `/home/user/organize.sh` that performs this entire process, and then execute it. The environment is standard Linux; you may use standard tools like `awk`, `grep`, `tr`, `sort`, `bc`, etc.