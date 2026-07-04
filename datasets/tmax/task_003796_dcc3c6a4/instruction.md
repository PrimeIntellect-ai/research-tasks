You are a data analyst stepping into a project left by a previous engineer. We have a set of CSV files representing a simple social e-commerce knowledge graph: users, their friendships, and their product purchases.

Your goal is to find the most "socially shared" products. A product is "socially shared" if two users who are **friends** both purchased it. 
For example, if User A and User B are friends, and both bought Product X, that counts as 1 shared instance for Product X. (If A, B, and C are all mutual friends and all bought X, that's 3 instances: A-B, B-C, A-C).

The previous engineer wrote a C++ program to compute this and output the top 4 products sorted by shared instances (descending), breaking ties by `product_id` (ascending). 
However, their code has a severe bug: it incorrectly calculates an implicit cross-join of all users who bought a product, completely ignoring whether they are actually friends in the `friends.csv` file! This results in massively inflated counts.

Your task:
1. Navigate to `/home/user/project/`.
2. Inspect the `data/` directory containing `users.csv`, `friends.csv`, and `purchases.csv`. 
   - `friends.csv` is provided as `user1,user2` (assume friendships are undirected, so if 1 is friends with 2, 2 is friends with 1).
   - `purchases.csv` is provided as `user_id,product_id`.
3. Fix the C++ code in `src/analyzer.cpp` to properly match the knowledge graph pattern: it must only count pairs of users who bought the same product AND are friends. Ensure each pair of friends is only counted once per product.
4. Compile the program using the provided `Makefile` by running `make`.
5. Run the compiled program so that it writes the correct aggregated, sorted, and paginated results (top 4) to `/home/user/output/report.csv`.

The output file `/home/user/output/report.csv` must follow exactly this format (no headers):
```csv
product_id,shared_count
```

Do not change the `Makefile` or the names/locations of the data files. Just fix the logic in `src/analyzer.cpp`, compile, and run it to produce the correct report.