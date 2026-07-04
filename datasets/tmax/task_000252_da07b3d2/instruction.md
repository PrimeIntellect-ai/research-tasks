You are a data engineer building the final stage of an ETL pipeline that processes text documents, generates embeddings using a simplified custom model, reduces their dimensionality, and retrieves the most relevant documents based on a query vector.

You need to write a Go program (using only the standard library) that performs this exact pipeline. 

**System Setup & Inputs:**
- **Documents:** A directory `/home/user/etl_data/` contains several text files (`.txt`).
- **Vocabulary:** `/home/user/model/vocab.json` contains a JSON mapping of words (strings) to their 5-dimensional embeddings (arrays of 5 floats).
- **Projection Matrix:** `/home/user/model/projection.csv` contains a 5x2 matrix (5 rows, 2 columns, comma-separated) used for dimensionality reduction.

**Your Go Program (`/home/user/pipeline.go`) must implement the following logic:**

1. **Embedding Computation:**
   For each `.txt` document in `/home/user/etl_data/`:
   - Tokenize the text by converting it to lowercase and splitting by standard whitespace (do not worry about punctuation stripping, the test documents are pre-cleaned and only contain lowercase letters and spaces).
   - Find the embedding for each word in `vocab.json`. Ignore any words that do not exist in the vocabulary.
   - Compute the *Document Embedding* (a 1x5 vector) by calculating the element-wise average of the embeddings of all known words in the document. If a document has no known words, its embedding is `[0.0, 0.0, 0.0, 0.0, 0.0]`.

2. **Dimensionality Reduction:**
   - Multiply the 1x5 Document Embedding by the 5x2 Projection Matrix.
   - The result is a 1x2 *Reduced Vector* `[x, y]` for the document.
   - Specifically: `Reduced[j] = sum(Document[i] * Matrix[i][j])` for `i` in 0..4 and `j` in 0..1.

3. **Retrieval:**
   - The query you are targeting has a reduced vector of exactly: `[0.85, -0.15]`
   - Calculate the Euclidean distance between each document's Reduced Vector and the query vector.
   - Identify the top 3 documents that are *closest* to the query vector (smallest distance).

**Output Requirements:**
Write the filenames of the top 3 closest documents (just the filename, e.g., `doc14.txt`) to `/home/user/top_docs.txt`, ordered from closest (line 1) to 3rd closest (line 3).
Tie-breaking: If distances are perfectly equal, order them alphabetically by filename.

To complete the task, write your code, execute it, and ensure `/home/user/top_docs.txt` is created with the correct format.