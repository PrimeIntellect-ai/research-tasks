You are a Machine Learning Engineer preparing training data. We need a lightweight tool to find similar documents based on a primitive bag-of-words embedding. 

Write a Go program located at `/home/user/embed.go` that accomplishes the following:

1. **Schema Enforcement**: Read a JSON-lines dataset from `/home/user/raw_data.jsonl`. Each line should be a JSON object. Only process lines that contain both an `"id"` (string) and a `"description"` (string). Ignore any lines missing either of these fields or containing malformed JSON.
2. **Embedding Computation**: For each valid document, compute a 5-dimensional feature vector based on the occurrence counts of the following exactly matched substrings (case-insensitive) in the `"description"` field, in this exact order: 
   `["machine", "learning", "data", "science", "algorithm"]`.
   *Hint: You can just use simple case-insensitive substring counting, equivalent to Go's `strings.Count(strings.ToLower(desc), keyword)`.*
3. **Similarity Search**: The program should accept a target `id` as the first command-line argument (e.g., `go run /home/user/embed.go doc4`). It must compute the Cosine Similarity between the target document's vector and all *other* valid documents' vectors. (If a vector has a magnitude of 0, the similarity is 0).
4. **Experiment Tracking**: Find the document with the highest cosine similarity to the target document. If there's a tie, choose the document that appeared first in the file. Write the result to `/home/user/result.json` as a JSON object with the following schema:
   ```json
   {
     "target_id": "doc4",
     "similar_id": "doc1",
     "score": 0.816
   }
   ```
   The `score` must be a float rounded to exactly 3 decimal places.

Run your Go program for the target id `doc4` to generate the final `/home/user/result.json` file.