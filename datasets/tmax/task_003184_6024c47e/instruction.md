You are assisting a data science researcher who is organizing a large, messy directory of dataset metadata. The researcher wants to test a semantic search pipeline to find datasets that match specific research queries.

Your task is to build a Python pipeline that reads several dataset descriptions, computes their semantic embeddings, and retrieves the most relevant datasets for a specific query.

Here are the requirements:
1. **Input Data**: The dataset descriptions are located in `/home/user/dataset_metadata/`. Each file is a `.txt` file containing a short description of a dataset.
2. **Model**: You must use the `all-MiniLM-L6-v2` model from the `sentence-transformers` library to compute the embeddings. You will need to install the necessary dependencies yourself.
3. **Query**: The researcher wants to find datasets similar to this query: *"Medical chest X-ray images for pneumonia detection and classification"*
4. **Similarity Search**: Compute the cosine similarity between the query embedding and the embeddings of all dataset descriptions.
5. **Output**: Create a JSON file at `/home/user/results/top_matches.json` with the following format:
   ```json
   {
     "query": "Medical chest X-ray images for pneumonia detection and classification",
     "top_3_files": [
       "filename1.txt",
       "filename2.txt",
       "filename3.txt"
     ]
   }
   ```
   The `top_3_files` list must contain the exact filenames of the 3 most similar datasets, ordered from most similar to least similar. Ensure the `/home/user/results/` directory exists before writing the file.

Write the code, execute it, and verify that the output JSON is correctly formatted.