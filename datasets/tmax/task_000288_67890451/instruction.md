You are an AI assistant helping a data scientist clean a dataset of text sentences. 

There is a file located at `/home/user/raw_texts.txt` that contains one sentence per line. The dataset is noisy and contains near-duplicate sentences. Your task is to clean this dataset and extract its vocabulary.

Please perform the following steps:
1. Install any necessary dependencies. You may choose the programming language, but Python is recommended.
2. Load the sentences from `/home/user/raw_texts.txt`.
3. Compute dense embeddings for each sentence using the `sentence-transformers` package and the `all-MiniLM-L6-v2` model.
4. Iterate through the sentences in their original order. For each sentence, compute its cosine similarity with all previously kept sentences. If the similarity is greater than or equal to `0.85` with *any* previously kept sentence, discard it as a near-duplicate. Otherwise, keep it.
5. Save the kept sentences to `/home/user/cleaned_texts.txt`, preserving their original order, with one sentence per line.
6. Tokenize the *kept* sentences to build a vocabulary. Tokenization should be done by converting the text to lowercase and splitting it into words using non-alphanumeric characters as delimiters (e.g., matching `[a-z0-9]+`). 
7. Save the unique tokens (vocabulary), sorted alphabetically, to `/home/user/vocab.txt`, with one token per line. Filter out any empty string tokens.

Ensure both output files are created exactly at the specified paths.