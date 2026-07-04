You are an AI assistant helping a researcher organize their disorganized datasets.

The researcher has two datasets containing short text descriptions of scientific concepts, but they come from different sources and lack a common key. 

Dataset A is located at `/home/user/dataset_A.csv` and has the columns: `id`, `title`, `abstract`.
Dataset B is located at `/home/user/dataset_B.json` and is an array of objects with keys: `doc_id`, `text`.

Your task is to match each record in Dataset A to the most semantically similar record in Dataset B using TF-IDF "embeddings" and cosine similarity. 

Please perform the following steps:
1. Read both datasets.
2. Preprocess the `abstract` from Dataset A and the `text` from Dataset B using this exact tokenization strategy:
   - Convert all text to lowercase.
   - Remove all punctuation (keep only alphanumeric characters and spaces).
   - Split into tokens by whitespace and join them back with a single space.
3. Compute TF-IDF vectors for the combined corpus of all preprocessed texts (from both datasets) so they share the same vocabulary. You may use Python's `scikit-learn` library.
4. Compute the cosine similarity between the TF-IDF vector of each abstract in Dataset A and every text in Dataset B.
5. For each `id` in Dataset A, find the `doc_id` in Dataset B that has the highest cosine similarity.
6. Create a joined dataset and save it to `/home/user/matches.csv`. The file must contain exactly two columns: `A_id` and `B_doc_id`, separated by a comma, including a header row. Order the rows by `A_id` ascending.

Make sure your final file is formatted exactly as requested.