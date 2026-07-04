You are an automation specialist setting up a data processing pipeline for an e-commerce inventory system. We have a legacy export of product attributes in a "wide" CSV format, and we need to process it, find similarities, and load the results into a relational database.

Your task is to create a complete workflow that does the following:

1. **Read the Input File:**
   There is a file located at `/home/user/products_wide.csv`. It contains product attributes with columns: `item_id, attr_color, attr_taste, attr_category`.

2. **Reshape and Normalize (Wide to Long):**
   Transform the wide data into a long format where columns are `item_id, attribute_name, text`.
   For each text value, normalize it by converting to lowercase and removing all punctuation (keep only alphanumeric characters and spaces). Then tokenize the text by splitting on spaces into a set of unique words.

3. **Compute Similarity:**
   For every possible pair of *different* `item_id`s (where `item_id_A` < `item_id_B` lexicographically), compare their normalized tokens *for each attribute separately*.
   Compute the Jaccard similarity score for the token sets. Jaccard similarity is the size of the intersection divided by the size of the union of the two sets. If both sets are empty, the similarity is 0.0.
   Filter the results to keep only pairs where the similarity score is greater than or equal to `0.4`.

4. **Export to CSV:**
   Save the filtered results to `/home/user/similarities.csv` without a header row.
   The format must strictly be: `item_id_A,item_id_B,attribute_name,similarity_score`
   Ensure the `similarity_score` is formatted to exactly 2 decimal places (e.g., `0.50`).

5. **Bulk Import to Database:**
   Create an SQLite database at `/home/user/inventory.db`.
   Create a table named `similarity_network` with the schema:
   `CREATE TABLE similarity_network (item_1 TEXT, item_2 TEXT, attribute TEXT, score REAL);`
   Use SQLite's bulk import feature (e.g., `.import`) to load `/home/user/similarities.csv` into this table.

Complete this workflow using bash commands, SQLite commands, and a scripting language of your choice (Python is recommended).