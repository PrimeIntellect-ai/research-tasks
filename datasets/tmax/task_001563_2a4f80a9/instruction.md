You are an automation specialist tasked with building a data processing pipeline to analyze customer reviews. The raw data is located at `/home/user/raw_reviews.txt`.

You must implement a pipeline using Python scripts and a `Makefile` to orchestrate the workflow as a DAG.

**Pipeline Specifications:**

1. **Extraction (`extract.py`):**
   - Read `/home/user/raw_reviews.txt`.
   - Each line has the format: `ID:<id> | TEXT:<review_text> | META:<messy_metadata>`
   - Use regex to extract the rating (an integer from 1 to 5) from the `META` section. The rating will appear in one of these three formats: `rating:X`, `X stars`, or `score=X` (where X is the digit).
   - Write the parsed data to `/home/user/extracted.csv` with columns: `id,rating,text`. The `id` should be an integer. Keep the text exactly as it appears.

2. **Stratified Sampling (`sample.py`):**
   - Read `/home/user/extracted.csv`.
   - Perform deterministic stratified sampling: for each rating (1 through 5), sort the records by `id` in ascending order, and select exactly the first 5 records. You should end up with exactly 25 records.
   - Write these 25 records to `/home/user/sampled.csv` in the same format.

3. **Parallel Similarity Computation (`similarity.py`):**
   - Read `/home/user/sampled.csv`.
   - Compute the character-trigram Jaccard similarity between all unique pairs of these 25 reviews.
   - You MUST use Python's `multiprocessing` module to parallelize these pairwise comparisons.
   - Trigram definition: A set of overlapping contiguous sequences of 3 characters from the exact review text (case-sensitive, spaces included). E.g., "Hello" -> `{"Hel", "ell", "llo"}`.
   - Jaccard similarity: `length(intersection) / length(union)`.
   - Find all pairs where the similarity is `>= 0.4`.
   - Output a JSON array of these pairs to `/home/user/similar_pairs.json`. Each pair should be a list `[id1, id2]` where `id1 < id2`. The overall JSON list must be sorted primarily by `id1` ascending, and secondarily by `id2` ascending.

4. **Orchestration (`Makefile`):**
   - Create a `Makefile` in `/home/user/` that defines the DAG.
   - Target `extracted.csv` depends on `raw_reviews.txt` and `extract.py`.
   - Target `sampled.csv` depends on `extracted.csv` and `sample.py`.
   - Target `similar_pairs.json` depends on `sampled.csv` and `similarity.py`.
   - Target `all` (the default) depends on `similar_pairs.json`.

You should be able to run `make` in `/home/user/` and it will execute the full pipeline, ultimately producing `/home/user/similar_pairs.json`.