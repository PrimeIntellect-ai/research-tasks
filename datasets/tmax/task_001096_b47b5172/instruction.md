You are a data analyst tasked with processing a dataset of text documents to find the most similar pairs based on their vocabulary. 

You need to build a multi-language pipeline (Bash + Python) to clean the data, tokenize it, and use linear algebra to compute similarities.

Here is your workflow:

1. **Dependency Installation**: Ensure `numpy` is installed in your Python environment. You may install it using pip.
2. **Data Cleaning (Bash/Shell)**:
   You are given a raw dataset at `/home/user/raw_data.csv` with two columns: `id,text`. 
   Using shell utilities (like `sed`, `awk`, or `tr`), create a cleaned file at `/home/user/cleaned_data.csv`. 
   The cleaning rules for the `text` column are:
   - Convert all characters to lowercase.
   - Remove all punctuation characters (only keep English letters `a-z`, numbers `0-9`, and spaces).
   - Preserve the comma `,` that separates the `id` and the `text` column. Do not remove or alter the header `id,text`.
   - Ensure consecutive spaces are reduced to a single space, and strip leading/trailing spaces from the text if any.

3. **Tokenization and Linear Algebra (Python)**:
   Write a Python script that reads `/home/user/cleaned_data.csv`.
   - **Tokenize**: Split the text of each document by space to form tokens.
   - **Vectorize**: Build a Document-Term Matrix (DTM) where rows represent documents and columns represent unique words across the entire corpus. The values should be raw term frequencies (TF) - i.e., the count of each word in the document.
   - **Compute Similarity**: Using `numpy` and linear algebra operations (matrix multiplication and norms), compute the pairwise Cosine Similarity between all documents. 

4. **Reporting**:
   Identify the top 3 most similar *distinct* document pairs (where `id1 < id2` to avoid duplicates and self-similarity).
   Write these top 3 pairs to a file named `/home/user/top_pairs.csv` with the exact header `id1,id2,similarity`.
   Format the `similarity` score rounded to exactly 4 decimal places. The file should be sorted in descending order of similarity.

All scripts should be executed to produce the final `/home/user/top_pairs.csv` file. Do not use external ML libraries like `scikit-learn`; rely on `numpy` for the math.