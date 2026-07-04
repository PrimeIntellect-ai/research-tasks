You are an assistant helping a researcher organize and analyze a text dataset. The researcher has a collection of document titles and wants to find the two most similar documents using linear algebra techniques.

Your task is to write a C++ program that processes the dataset, computes a Document-Term Matrix (DTM), and finds the most similar pair of documents based on cosine similarity.

Here are the requirements:
1. Create a C++ source file at `/home/user/analyze.cpp`.
2. The program must read a text dataset from `/home/user/titles.txt`, where each line represents a single document (0-indexed).
3. **Tokenization & Preprocessing:**
   - Tokenize each line by whitespace.
   - Convert all characters to lowercase.
   - Remove all non-alphanumeric characters from the tokens (e.g., "c++" becomes "c", "data-driven" becomes "datadriven").
   - Discard any empty tokens that result from this process.
4. **Vectorization (Linear Algebra):**
   - Build a vocabulary of all unique tokens across the entire corpus, sorted alphabetically.
   - Construct a Term-Frequency (TF) vector for each document. The length of the vector is the size of the vocabulary. Each element represents the count of a specific word in that document.
   - L2-normalize each document's TF vector. (Divide each element by the Euclidean norm of the vector. If the norm is 0, leave the vector as all zeros).
5. **Similarity Computation:**
   - Compute the document-document cosine similarity matrix. Since the vectors are already L2-normalized, the cosine similarity between Document A and Document B is simply their dot product.
   - Find the distinct pair of documents `i` and `j` (where `i < j`) that have the maximum cosine similarity.
   - If there is a tie for the highest similarity, select the pair with the smallest `i`. If there is still a tie, select the pair with the smallest `j`.
6. Write the final result to `/home/user/result.txt` containing exactly one line in this format:
   `[i] [j] [similarity_score]`
   Format the similarity score to exactly 4 decimal places (e.g., `0 4 0.6124`).

Once you have written `/home/user/analyze.cpp`, compile it using `g++ -std=c++17 -O3 analyze.cpp -o analyze` and run it to produce `/home/user/result.txt`.