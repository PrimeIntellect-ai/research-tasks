You are a data engineer building a fast ETL pipeline for log analysis. We need to find historical log events that are most similar to a specific target error message using Jaccard similarity. Because this runs on massive files in production, the similarity search must be implemented in C, while the dataset preparation should be done using standard Bash utilities.

Your task is to build a reproducible pipeline that does the following:

1. **Dataset Preparation**: 
   You will find a file at `/home/user/raw_logs.csv`. Its format is `id,timestamp,raw_message`.
   Write a bash script or command that extracts only the `raw_message` column, converts all text to lowercase, and replaces all non-alphanumeric characters with a single space (collapsing multiple spaces into one). 
   Save this cleaned dataset to `/home/user/clean_logs.txt` (one message per line).

2. **Similarity Search in C**:
   Write a C program at `/home/user/jaccard.c` and compile it to `/home/user/jaccard`.
   The program should take exactly one command-line argument: a target query string.
   It should read the cleaned dataset from standard input (stdin), one line at a time.
   For each line, it should compute the Jaccard similarity between the words in the query and the words in the line. 
   *Note: Jaccard similarity is (Intersection of unique words) / (Union of unique words).*
   The program should print ONLY the exact line from the input that has the highest Jaccard similarity score. If there is a tie, print the first one encountered.

3. **Execution**:
   The target query is: `"critical server overload crash"`
   Run your compiled C program against `/home/user/clean_logs.txt` using this target query.
   Save the single best matching line to `/home/user/best_match.txt`.

Ensure your C code compiles cleanly with `gcc /home/user/jaccard.c -o /home/user/jaccard`.