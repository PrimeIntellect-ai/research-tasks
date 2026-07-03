You are an MLOps engineer tasked with tracking experiment artifacts for a document deduplication pipeline. The previous pipeline had numerical instability issues and lacked automated validation. 

Your objective is to build a robust embedding computation, retrieval, and validation script.

Here are your instructions:

1. Set up your workspace: Create a directory at `/home/user/mlops_workspace`. We have provided a corpus of documents at `/home/user/mlops_workspace/corpus.json` (you assume it exists, it will be generated before you start). The file contains a JSON list of strings (the documents).
2. Install necessary dependencies. You will need `numpy`, `scikit-learn`, and `pytest`.
3. Write a Python script named `/home/user/mlops_workspace/compute_retrieval.py` that does the following:
   - Loads the documents from `corpus.json`.
   - Computes text embeddings using `sklearn.feature_extraction.text.TfidfVectorizer` (use `stop_words='english'` and default parameters).
   - Computes the pairwise Cosine Similarity between all document embeddings.
   - For every document, identifies the most similar *other* document (ignoring itself).
   - Filters the results to only include pairs where the Cosine Similarity is `>= 0.80`.
   - Deduplicates the pairs (so `[A, B]` and `[B, A]` only appear once, keeping the one where the first index is smaller).
   - Outputs the results to `/home/user/mlops_workspace/retrieved_pairs.json` in the exact format: `[[index1, index2, similarity_score], ...]`. The list must be sorted by `similarity_score` in descending order. Round the similarity score to 4 decimal places before saving.
4. Write a numerical accuracy and validation test file at `/home/user/mlops_workspace/test_accuracy.py` using `pytest`. The test must:
   - Load `/home/user/mlops_workspace/retrieved_pairs.json`.
   - Have a test function `test_numerical_bounds()` that asserts every similarity score is strictly `<= 1.0001` and `>= 0.7999` (to account for minor floating point rounding).
   - Have a test function `test_schema()` that asserts each item is a list of length 3, where the first two elements are integers and the third is a float.
5. Run your test suite. Your `test_accuracy.py` must pass successfully. Leave the files exactly where they are.