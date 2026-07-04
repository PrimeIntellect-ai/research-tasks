I am a researcher organizing a dataset of documents. I have pre-computed embeddings for 100 documents, located in `/home/user/embeddings.csv` (100 rows, 10 columns, no header). I also have a linear projection matrix to reduce the dimensionality of these embeddings for visualization and fast similarity search, located in `/home/user/projection.csv` (10 rows, 3 columns, no header).

Please write a Go program named `/home/user/process.go` that performs the following:
1. **Dimensionality Reduction**: Read both CSV files and reduce the dimensionality of the document embeddings by performing a matrix multiplication: `Reduced_Embeddings = Embeddings * Projection`. The resulting matrix should be 100x3.
2. **Similarity Search and Recommendation**: For each of the 100 documents (using their row index 0 to 99), find the top 2 *most similar* documents in the reduced 3D space. Similarity is defined by having the lowest Euclidean distance.
3. **Validation**: Ensure that a document is never recommended to itself (exclude the document's own index from its recommendations).
4. **Output**: Save the recommendations to `/home/user/recommendations.json`. The format must be a JSON object where the key is the string representation of the document's row index (e.g., `"0"`, `"1"`, ...) and the value is a JSON array of two integers representing the row indices of the 1st and 2nd closest documents, respectively.

Example of expected JSON structure in `/home/user/recommendations.json`:
```json
{
  "0": [45, 12],
  "1": [89, 2],
  ...
}
```

Once you have written the Go program, compile and run it to produce the `recommendations.json` file.