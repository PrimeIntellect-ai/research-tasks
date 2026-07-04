You are a data engineer tasked with building a high-performance C++ ETL pipeline component to identify duplicate product listings in a messy catalog.

You have been provided with a raw data file at `/home/user/products.txt`. Each line contains a product ID and a raw, messy description, separated by a pipe character `|`.

Your objective is to write and execute a C++ program (`/home/user/dedup.cpp`) that performs the following steps:
1. **Parse & Clean (Regex/Normalization):** For each line, separate the ID and the description. Clean the description by:
   - Converting all text to lowercase.
   - Using regular expressions to remove any HTML tags (e.g., `<p>`, `</b>`).
   - Removing all non-alphanumeric characters (except spaces).
   - Collapsing multiple consecutive spaces into a single space, and trimming leading/trailing spaces.
2. **Similarity Computation:** Compute the Jaccard similarity of the unique words between every possible pair of products. Jaccard similarity is defined as the size of the intersection of unique words divided by the size of the union of unique words.
3. **Parallel Processing:** The pairwise similarity computation must be parallelized to ensure fast execution (e.g., using OpenMP `#pragma omp parallel for` or C++ `std::thread` / `std::async`).
4. **Deduplication Output:** Identify all pairs of products with a Jaccard similarity strictly greater than `0.75`. 
   
Output the duplicate pairs to `/home/user/duplicates.csv`. 
- Each line must contain exactly two IDs separated by a comma: `ID1,ID2`.
- For each pair, `ID1` must be lexicographically less than `ID2` (e.g., `A123,B456`).
- The lines in the output file must be sorted lexicographically by `ID1`, then by `ID2`.

Compile your C++ program using `g++ -O3 -std=c++17 dedup.cpp -o dedup` (add `-fopenmp` or `-pthread` as needed) and run it to produce the final `duplicates.csv`.