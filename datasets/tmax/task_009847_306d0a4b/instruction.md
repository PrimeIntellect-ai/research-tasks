You are a data analyst working with a dataset of mathematical text descriptions. Your goal is to process a CSV file, compute a simple character-level frequency "embedding" for each text, and perform a similarity search to find the two most similar texts.

You must implement this pipeline in **C**.

**Input Data:**
A CSV file located at `/home/user/math_texts.csv` with the schema `id,text`. 
- `id` is an integer.
- `text` is a string containing mathematical descriptions (may contain spaces and punctuation).

**Task Requirements:**
1. Write a C program at `/home/user/find_similar.c`.
2. The program must read `/home/user/math_texts.csv`.
3. **Embedding Computation**: For each text, compute a 26-dimensional integer vector representing the frequency of the letters 'a' through 'z' (case-insensitive). Ignore spaces, numbers, and punctuation. For example, the text "Ab c!" would have an embedding where the first dimension (for 'A') is 1, the second ('B') is 1, the third ('C') is 1, and all others are 0.
4. **Similarity Search**: Compute the similarity between all pairs of distinct rows using the **Dot Product** of their 26-dimensional embedding vectors.
5. Find the pair of distinct texts (with IDs `A` and `B`, where `A < B`) that have the **maximum** dot product. If there is a tie, pick the pair with the smallest `A`. If there is still a tie, pick the pair with the smallest `B`.
6. Compile your program (e.g., using `gcc`) and execute it.
7. **Output**: Your C program must write the result to a file at `/home/user/result.txt`. The file should contain exactly one line with the format: `A,B,score` (where A and B are the IDs of the most similar pair, and score is their dot product integer value).

Ensure your C code enforces the data schema properly and handles the tokenization and vector computation efficiently.