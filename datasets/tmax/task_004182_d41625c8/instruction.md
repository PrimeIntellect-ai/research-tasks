You are a data engineer responsible for building a multi-stage ETL pipeline to process a messy product catalog. 

You have been provided with a raw dataset at `/home/user/raw_products.csv`. This file contains product information in a "wide" format, with multiple columns representing different localized translations for each product. The columns are:
`vendor_id, name_en, desc_en, name_fr, desc_fr, name_es, desc_es`

Your task is to build a Python-based ETL pipeline that performs the following steps:

1. **Reshape (Wide to Long):** Read `/home/user/raw_products.csv` and reshape it into a "long" format. The resulting format should have the following logical columns:
   `vendor_id, language, product_name, description`
   Where `language` is either `en`, `fr`, or `es`. Ignore any entries where the `product_name` is empty or null.

2. **Similarity Computation & Parallel Processing:** We need to find near-duplicate products within the same language. Using Python's `multiprocessing` or `concurrent.futures` module, parallelize a process that computes the string similarity between all pairs of `product_name`s *within the same language*. 
   * Use `difflib.SequenceMatcher(None, name1, name2).ratio()` as your similarity metric.
   * A pair is considered a "near-duplicate" if the similarity ratio is `>= 0.85`.
   * Only compare products within the same language.
   * To avoid duplicate pairs, ensure `vendor_id_1 < vendor_id_2` (string comparison).

3. **Database Bulk Load:** 
   * Create a SQLite database at `/home/user/etl_results.db`.
   * Create two tables:
     * `long_products` (vendor_id TEXT, language TEXT, product_name TEXT, description TEXT)
     * `similar_pairs` (vendor_id_1 TEXT, vendor_id_2 TEXT, language TEXT, similarity_score REAL)
   * Use Python's SQLite3 executemany or bulk import features to load your reshaped data into `long_products` and your near-duplicate results into `similar_pairs`.

4. **Pipeline Output:** 
   * Finally, generate a summary file at `/home/user/summary.json` containing the total count of near-duplicate pairs found for each language. The JSON should look exactly like this:
     ```json
     {
       "en": 12,
       "fr": 5,
       "es": 0
     }
     ```

**Constraints:**
- Write your pipeline in Python (save it as `/home/user/pipeline.py` and run it).
- You must use parallel processing for the similarity computation step.
- Ensure the SQLite database and the JSON file are saved exactly at the paths specified.