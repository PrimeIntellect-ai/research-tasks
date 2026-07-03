You are helping a researcher who is trying to organize and classify a dataset of research paper abstracts. The previous researcher attempted to build a text classifier but made a critical error: they calculated the vocabulary and word frequencies across the *entire* dataset before splitting it, causing data leakage between the training and test sets. 

Your task is to fix this by building a Naive Bayes classifier entirely in **Bash** (using standard tools like `awk`, `grep`, `sed`, `bc`, etc.) that properly isolates the training data.

The dataset is located at `/home/user/research_data/dataset.csv`. It has the following columns: `id,split,label,text`
- `id`: A unique integer.
- `split`: Either `train` or `test`.
- `label`: Either `A` or `B` (for the test set, the label is given as `?`).
- `text`: A short space-separated string representing the abstract.

You must create a bash script at `/home/user/run_pipeline.sh` that does the following:

**1. Feature Engineering (Strictly on the Training Set):**
Extract all words from the `text` column where `split` is `train`. 
- Convert all words to lowercase.
- Ignore words with fewer than 4 characters.
- Find the **top 10 most frequent words** in the training set overall. If there is a tie, sort them alphabetically. These 10 words will be your "features".

**2. Bayesian Model Training:**
Using ONLY the training set and the 10 feature words, compute the parameters for a Multinomial Naive Bayes model.
- Calculate the prior probabilities $P(Class = A)$ and $P(Class = B)$ based on the training set class distribution.
- Calculate the conditional probabilities $P(Word = w | Class = C)$ for each of the 10 features and each class. 
- Use Laplace (+1) smoothing: $P(w|C) = \frac{count(w, C) + 1}{Total\_Words(C) + V}$, where $Total\_Words(C)$ is the total occurrences of *all 10 feature words* in class C, and $V = 10$ is the vocabulary size. 

**3. Model Inference:**
For each row in the dataset where `split` is `test`:
- Calculate the unnormalized log-posterior for Class A and Class B using the features present in the test text (only considering words that are in your top 10 feature list).
- $Score(C) = \ln(P(C)) + \sum_{w \in text \cap features} \ln(P(w|C))$
- Predict the class with the higher score. (In case of a tie, predict `A`).

**4. Output:**
Your script `/home/user/run_pipeline.sh` must write the predictions to `/home/user/predictions.csv`.
The file must have exactly the format:
```csv
id,prediction
101,A
102,B
...
```

Requirements:
- Ensure your script is executable (`chmod +x`).
- Do not use Python, R, or any external machine learning libraries. All logic must be implemented using Bash and standard POSIX utilities (awk is highly recommended for the math).
- Precision: Compute logarithms to at least 4 decimal places (e.g., using `awk '{print log($1)}'`).