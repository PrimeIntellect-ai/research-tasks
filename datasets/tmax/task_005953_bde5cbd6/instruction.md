You are an AI assistant helping a machine learning researcher organize a new text dataset and verify the numerical accuracy of a basic embedding pipeline. 

The researcher has provided a raw text file located at `/home/user/corpus.txt`.

Your task is to write a Python script that performs tokenization, dataset preparation, and a basic model evaluation (an embedding bag forward pass), and then outputs the results to `/home/user/output.json`.

Here are the exact requirements:

1. **Tokenization & Dataset Preparation**:
   - Read `/home/user/corpus.txt`.
   - Process the text line by line. For each line, convert it to lowercase and remove all punctuation (use the regex `[^\w\s]` to replace punctuation with an empty string).
   - Split the cleaned text by whitespace to get a list of tokens for each line.
   - Build a vocabulary across the entire corpus. The vocabulary must map each unique token to a unique integer ID.
   - The IDs must start at `0` and be assigned in **alphabetical order** of the tokens. (e.g., the alphabetically first word gets ID 0).

2. **Numerical Accuracy & Model Evaluation**:
   - Create a dummy embedding matrix for the vocabulary using `numpy`. 
   - Set the random seed strictly using `numpy.random.seed(42)`.
   - Initialize the embedding matrix as a uniform distribution between -1 and 1: `embeddings = numpy.random.uniform(-1, 1, (vocab_size, 16))`.
   - For each of the **first 5 lines** of the corpus:
     - Convert the line's tokens into a list of integer IDs.
     - Look up the embedding vector for each ID.
     - Compute the element-wise sum of these embedding vectors to get a single 16-dimensional vector representing the line. If a line has no tokens, its sum vector should be all zeros.
     - Calculate the mean of this 16-dimensional sum vector.

3. **Output Format**:
   - Save the results to `/home/user/output.json` with the following strict structure:
     ```json
     {
       "vocab_size": <integer>,
       "first_5_lines": [
         {
           "line_index": <integer 0 to 4>,
           "token_ids": [<int>, <int>, ...],
           "embedding_sum_mean": <float rounded to exactly 4 decimal places>
         },
         ...
       ]
     }
     ```

Ensure your script handles everything end-to-end and successfully creates the JSON file. Do not use external libraries other than `numpy`, `json`, and built-in Python modules like `re`.