You are a data engineer debugging an ETL pipeline that handles multi-lingual customer feedback. Due to a retry-logic bug, the pipeline has produced duplicate records. You need to write a Python script to deduplicate the data and calculate a mathematical similarity metric to help identify "near-miss" duplicate clusters.

Your task is to process the file `/home/user/input/retries.tsv`.
This file has two tab-separated columns: `timestamp` and `payload_text`. The text contains multi-lingual Unicode characters and emojis.

Write a Python script that performs the following pipeline in order:

1. **Hash-based Deduplication**: 
   Iterate through the file sequentially. Compute the SHA256 hash of each `payload_text` (encoded as UTF-8). 
   Keep only the *first* occurrence of each unique `payload_text`. Discard any subsequent rows with the same text.

2. **Distance/Similarity Computation**:
   For the sequence of deduplicated texts, compute the Jaccard similarity of character **bigrams** between texts. 
   - A character bigram is any sequence of 2 adjacent characters (including spaces and punctuation).
   - Jaccard similarity between two sets of bigrams A and B is defined as `|A ∩ B| / |A ∪ B|`. 
   - If both sets are empty, their similarity is `1.0`.

3. **Windowed Aggregation**:
   Calculate a rolling average of this Jaccard similarity for each text against its recent predecessors.
   For the text at index `i` (in the deduplicated list), the rolling similarity is the average of the Jaccard similarities between `text_i` and up to `2` immediately preceding texts (`text_{i-1}` and `text_{i-2}`).
   - If `i = 0` (the first item), the rolling average is `0.0000`.
   - If `i = 1`, the rolling average is just the similarity to `text_0`.
   - If `i >= 2`, the rolling average is `(Jaccard(text_i, text_{i-1}) + Jaccard(text_i, text_{i-2})) / 2.0`.

Write the results to `/home/user/output/metrics.csv` with the header `hash,rolling_similarity`. 
Output the SHA256 hash (hex digest) and the rolling similarity rounded to exactly 4 decimal places (e.g., `0.0833`).

**Constraints & Details:**
- Standard Python libraries only (no pandas, numpy, or external libraries).
- Create the `/home/user/output/` directory if it does not exist.
- Ensure proper UTF-8 handling for reading and hashing.