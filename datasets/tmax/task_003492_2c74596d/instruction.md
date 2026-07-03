You are a Machine Learning Engineer preparing a retrieval dataset. Your goal is to process a raw text corpus, find the most relevant documents for a set of queries using similarity search, and compute statistical confidence intervals on the retrieval scores.

You must write a C++ program at `/home/user/process.cpp` to perform the following steps:

1. **Tokenization and Dataset Preparation**:
   Read two files:
   - `/home/user/corpus.txt`: Each line is a document in the corpus.
   - `/home/user/queries.txt`: Each line is a search query.
   
   Tokenize each line (from both files) using the following exact rules:
   - Convert all uppercase letters (`A-Z`) to lowercase (`a-z`).
   - Remove all characters EXCEPT lowercase letters (`a-z`), digits (`0-9`), and spaces (` `).
   - Split the resulting string into tokens by single spaces. Ignore empty tokens.
   - Represent each document and query as a Bag-of-Words (BoW) vector (term frequencies).

2. **Similarity Search**:
   For each query, compute the Cosine Similarity between the query's BoW vector and every document's BoW vector in the corpus. 
   Find the "Top-1" matching document (the one with the highest cosine similarity) for each query.
   *(Assume no query will result in a zero-vector and there will be no exact ties for the maximum similarity, or if there is, pick the one with the lowest line index).*

3. **Hypothesis Testing & Confidence Intervals**:
   Let $S$ be the set of the Top-1 cosine similarity scores for all queries (one score per query).
   Compute the sample mean ($\bar{x}$) and the sample standard deviation ($s$) of $S$.
   Compute the 95% Confidence Interval for the mean using the formula:
   $CI = \bar{x} \pm 1.96 \times \frac{s}{\sqrt{N}}$
   where $N$ is the number of queries.

4. **Output formatting**:
   Your C++ program must write the results to `/home/user/summary.csv` with the exact following format (scores formatted to 4 decimal places):
   
   ```csv
   QueryIndex,TopCorpusIndex,CosineSimilarity
   0,4,0.8165
   1,2,0.5000
   ...
   Mean,CI_Lower,CI_Upper
   0.6582,0.5210,0.7954
   ```
   *(Note: The numbers above are just structural examples, not the actual answers).*

Compile your code using `g++ -std=c++17 -O3 /home/user/process.cpp -o /home/user/process` and run it to produce the `summary.csv` file.