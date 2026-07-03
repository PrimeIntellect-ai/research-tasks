You are an AI assistant helping a researcher organize and validate a dataset of vector embeddings.

The researcher has a dataset of document embeddings located at `/home/user/data/embeddings.csv`. The CSV file has the header `id,v1,v2,v3,v4,v5`. 
They also have a baseline prediction file located at `/home/user/data/baseline.txt` which contains a single document ID representing a previous model's prediction for the closest document to `doc_73`.

Your task is to write and execute a Python script that does the following:
1. Loads the embeddings from `/home/user/data/embeddings.csv`.
2. Finds the top 3 closest documents to the target document `doc_73` using **Euclidean distance**. (Do not include `doc_73` itself in the results).
3. Orders these 3 documents from closest to furthest.
4. Reads the single ID from `/home/user/data/baseline.txt`.
5. Validates your results: If your #1 closest document ID exactly matches the ID in `baseline.txt`, the validation status is `MATCH`. Otherwise, it is `MISMATCH`.
6. Writes the final results to `/home/user/results.log`.

The format of `/home/user/results.log` must be exactly 4 lines:
- Line 1: The ID of the 1st closest document
- Line 2: The ID of the 2nd closest document
- Line 3: The ID of the 3rd closest document
- Line 4: The validation status (`MATCH` or `MISMATCH`)

You may use standard Python libraries. Please write the script, execute it, and ensure `/home/user/results.log` is created with the correct information.