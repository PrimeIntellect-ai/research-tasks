You are a data scientist cleaning and analyzing a dataset of product reviews. You need to write a Rust utility to perform tokenization, calculate document similarities, and compute basic statistical summaries.

The dataset is located at `/home/user/dataset.txt`, with one text entry per line. 

Your objective is to write a Rust program at `/home/user/processor.rs` that does the following:
1. Reads `/home/user/dataset.txt`.
2. Tokenizes each line: convert the text to lowercase, split by whitespace, and collect the unique words into a mathematical set (ignoring punctuation removal for this simple task, just split on whitespace).
3. Takes the very first line (Line 0) as the "query" document.
4. Calculates the Jaccard similarity between the query (Line 0) and all *other* lines (Line 1 to N-1). The Jaccard similarity is the size of the intersection divided by the size of the union of the two sets.
5. Computes the mean (average) Jaccard similarity across all these comparisons.
6. Identifies the top 3 most similar lines to Line 0. (If there is a tie in similarity, favor the smaller line index).
7. Outputs a file to `/home/user/summary.txt` with exactly the following format:
   ```
   Mean Similarity: X.XXXX
   Top 3: [Index1, Index2, Index3]
   ```
   *Note: `X.XXXX` must be the mean similarity rounded to exactly 4 decimal places (e.g., `0.3705`). The indices must be the line numbers (1-indexed relative to the whole file, or just the array index where Line 0 is the first line).*

Once your Rust script is ready, compile it using `rustc /home/user/processor.rs` and run it to produce `/home/user/summary.txt`.