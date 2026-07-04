You are a data analyst tasked with processing a dataset of text snippets to find similar documents using a Bag-of-Words (BoW) approach.

Your environment is missing some basic compilation tools. First, install `gcc` and `make` (you can use `sudo apt-get update && sudo apt-get install -y gcc make`).

You have two input files:
1. `/home/user/data/dataset.csv`: A CSV file with a header `id,text`. The text contains only lowercase letters and spaces.
2. `/home/user/data/vocab.txt`: A text file containing one vocabulary word per line.

Your objective is to write a C program at `/home/user/src/search.c` that does the following:
1. Reads both files.
2. Tokenizes the `text` field of each document by splitting on spaces.
3. Computes a term frequency (count) vector for each document based on the exact words in `vocab.txt`. 
4. Computes the cosine similarity between the document with `id=1` and all other documents in the dataset.
5. Identifies the top 3 most similar documents to document `id=1` (excluding document 1 itself).
6. Writes the results to `/home/user/output/results.csv` with the header `id,similarity`. 
   - The results must be sorted in descending order of similarity.
   - If there is a tie in similarity, sort those rows in ascending order by `id`.
   - The similarity values must be rounded to exactly 4 decimal places (e.g., `0.8944`).

Requirements for the C program:
- Ensure the output file is written exactly to `/home/user/output/results.csv`.
- Create any missing directories before writing.
- Compile your program using `gcc -O3 -lm /home/user/src/search.c -o /home/user/src/search` and then run it.

Please write, compile, and execute the C program to generate the required output file.