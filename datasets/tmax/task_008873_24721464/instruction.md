You are a Data Analyst working with a proprietary legacy sentiment analysis system. We lost the original inference code, but we still have the model weights, vocabulary, and a batch of new customer reviews to process. 

Your task is to reconstruct the model architecture in PyTorch, tokenize the dataset, compute the embeddings for the reviews, and find the most similar pairs of reviews based on their embeddings.

You are provided with a working directory structure under `/home/user/` that contains:
- `/home/user/data/reviews.csv`: A CSV file with two columns, `id` and `text`.
- `/home/user/model/vocab.json`: A dictionary mapping words to integer indices. Index `0` is always `<UNK>`.
- `/home/user/model/embeddings.npy`: A NumPy array of shape `(vocab_size, 32)` containing word embeddings.
- `/home/user/model/linear_w.npy`: A NumPy array of shape `(16, 32)` representing the weights of a linear projection layer.
- `/home/user/model/linear_b.npy`: A NumPy array of shape `(16,)` representing the biases of the linear projection layer.

You must build a reproducible pipeline by following these steps:

1. **Tokenization:**
   - Read `reviews.csv`.
   - For each text, convert it to lowercase.
   - Remove all punctuation (specifically, remove any character that matches the regex `[^\w\s]`).
   - Split the text into tokens by whitespace.
   - Map each token to its corresponding integer using `vocab.json`. If a word is not in the vocabulary, use `0` (`<UNK>`).

2. **Model Reconstruction & Inference:**
   - Write a PyTorch script to reconstruct the model. The model consists of:
     a) An embedding layer initialized with `embeddings.npy`.
     b) A mean pooling operation that averages the token embeddings for a given review. (If a review has 0 tokens, the mean pooled vector should be a zero vector of size 32).
     c) A Linear layer mapping from 32 dimensions to 16 dimensions, initialized with `linear_w.npy` and `linear_b.npy`.
     *Note: Do not use any non-linear activation functions.*
   - Pass all tokenized reviews through this model to get a 16-dimensional sentence embedding for each review.

3. **Similarity Computation:**
   - Compute the cosine similarity between all pairs of review embeddings.
   - Find the top 3 most similar *distinct* pairs of reviews (do not compare a review to itself).
   - If two pairs are equivalent (e.g., A-B and B-A), only consider the pair where the first ID is alphabetically less than the second ID.

4. **Reporting:**
   - Save the top 3 pairs to `/home/user/output/top_pairs.csv` with exactly the following columns: `id1,id2,similarity`.
   - Order the rows by similarity descending. If there is a tie, order by `id1` ascending, then `id2` ascending.
   - Round the similarity score to 4 decimal places.

5. **Reproducibility:**
   - Write your entire workflow into a bash script at `/home/user/run_pipeline.sh` so that running `bash /home/user/run_pipeline.sh` executes the full process from reading the data to generating the output file.

You may install any necessary Python packages (e.g., `torch`, `pandas`, `numpy`, `scikit-learn`) using `pip`.