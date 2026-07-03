You are a data engineer building a Go-based ETL pipeline. You have been given a dataset `/home/user/data.csv` containing item embeddings. However, the data is messy: it has missing values, outliers, and needs its dimensionality reduced before performing a similarity search.

Write and execute a Go program that performs the following steps:

1. **Parse the CSV:** Read `/home/user/data.csv` which has a header row `ID,f1,f2,f3,f4,f5,f6`.
2. **Missing Value Handling:** For any feature `f1` to `f6` that is missing (empty string), impute it with `0.0`.
3. **Dimensionality Reduction:** Reduce the 6 features into 3 new features (`R1, R2, R3`) by summing adjacent pairs:
   - `R1 = f1 + f2`
   - `R2 = f3 + f4`
   - `R3 = f5 + f6`
4. **Outlier Handling:** Clip the values of `R1, R2,` and `R3` to the range `[-10.0, 10.0]`. If a value is greater than 10.0, set it to 10.0. If it is less than -10.0, set it to -10.0.
5. **Similarity Search:** Find the target vector with ID `"TARGET"`. Compute the Euclidean distance between the `"TARGET"` vector and all other vectors in the reduced, clipped 3-dimensional space.
6. **Output:** Find the 3 records (excluding `"TARGET"`) that are most similar (lowest Euclidean distance) to `"TARGET"`. Write their IDs to `/home/user/top3.txt`, one ID per line, sorted from closest to farthest.

You may use standard Go libraries only.