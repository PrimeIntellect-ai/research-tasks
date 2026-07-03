You are an ETL Data Engineer. We have a raw dataset of support tickets that needs to be cleaned, embedded, and queried.

Your task is to write and run a Python script that implements the following pipeline:

1. **Environment Setup**: You will need to install the necessary Python packages. Use `pandas` for data manipulation, and `sentence-transformers` for embedding computation.
2. **Data Cleaning**: 
   Read the dataset located at `/home/user/tickets.csv`. The CSV has two columns: `ticket_id` and `text`.
   - **Missing Values**: Drop any rows where the `text` is missing (NaN, null, or strictly empty strings).
   - **Outlier Handling**: We consider texts that are too short or improperly long as anomalies. Drop any rows where the `text` is less than 15 characters long OR greater than 200 characters long.
3. **Embedding Computation**: 
   Using the `sentence-transformers` package, load the `all-MiniLM-L6-v2` model. Compute the embeddings for all the cleaned ticket texts.
4. **Retrieval**:
   We have a new incoming query: `"I forgot my login details and the reset email is not arriving."`
   Compute the embedding for this query using the same model. Calculate the cosine similarity between the query embedding and all the cleaned ticket embeddings.
5. **Output**:
   Find the `ticket_id` of the ticket that has the highest cosine similarity to the query.
   Write this single integer `ticket_id` to a file at `/home/user/best_match.txt`.

Do not write anything else to the output file, just the integer ID.