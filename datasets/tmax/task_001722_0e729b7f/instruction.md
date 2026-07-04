You are a data scientist cleaning a raw dataset of mathematical vectors and building a lightweight similarity recommendation pipeline using only Bash and standard GNU utilities.

You have a dataset located at `/home/user/data.csv`. The file has a header and contains 3-dimensional vectors in the format `ID,X,Y,Z`. Some rows are corrupted and contain `NA` values or empty strings in the vector columns.

Your task:
1. Write a shell command pipeline to clean the dataset by removing the header and any rows that contain `NA` or have missing coordinate values.
2. For the valid rows, calculate the Manhattan distance between each row's vector `(X, Y, Z)` and a target vector `(12, 19, 28)`.
   *The Manhattan distance between (X1, Y1, Z1) and (X2, Y2, Z2) is |X1 - X2| + |Y1 - Y2| + |Z1 - Z2|.*
3. To ensure your pipeline is perfectly reproducible, sort the results first by their Manhattan distance in ascending order, and break any distance ties by sorting by the `ID` in ascending order (numerically).
4. Extract the `ID`s of the top 3 most similar vectors (the ones with the smallest Manhattan distance to the target) and save these IDs, one per line, into a file at `/home/user/recommendations.txt`.

Do not use Python or other scripting languages; stick to standard CLI tools like `awk`, `sed`, `grep`, `sort`, `head`, etc.