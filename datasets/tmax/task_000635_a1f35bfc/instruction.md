You are a data engineer building a fast ETL pipeline filter in C. You need to process a stream of log messages to detect redundant or repetitive logs by computing similarities and tracking moving averages. 

Your task is to write a C program that reads a text file of log messages line-by-line, normalizes and tokenizes the text, calculates the Jaccard similarity between consecutive lines, and computes a rolling average of these similarity scores.

Here are the requirements for your C program (`/home/user/log_processor.c`):

1. **Tokenization & Normalization**:
   - For each line, extract words consisting only of alphanumeric characters (`A-Z`, `a-z`, `0-9`). Treat any contiguous sequence of alphanumeric characters as a single token.
   - Ignore all other characters (punctuation, whitespace, etc. act as delimiters).
   - Convert all extracted tokens to lowercase.
   - Keep only unique tokens for each line (i.e., a set of unique words per line).

2. **Distance & Similarity**:
   - Compute the Jaccard similarity between the unique token set of the *current* line and the unique token set of the *previous* line.
   - Jaccard similarity is defined as the size of the intersection divided by the size of the union of the two sets.
   - For the very first line, assume the "previous line" is an empty set. Thus, if the first line has tokens, the similarity is `0.0000`. If both sets are empty, the similarity is `1.0000`.

3. **Rolling Statistics**:
   - Compute the rolling average of the Jaccard similarity scores over a sliding window of the last 3 lines.
   - For line 1, the average is just the score of line 1.
   - For line 2, it is the average of the scores for line 1 and 2.
   - For line 3 and beyond, it is the average of the scores of the current line and the 2 preceding lines.

**Execution & Output Format**:
The program should read from a file named `/home/user/raw_logs.txt`.
It must output the results to `/home/user/rolling_sim.csv` in the exact CSV format below (including header), with floats formatted to 4 decimal places (`%.4f`).

CSV Header: `Line,Jaccard,Rolling_Avg`
Example row: `1,0.0000,0.0000`

I will place the input file at `/home/user/raw_logs.txt` with the following contents before you start:
```
Error: Disk full on /dev/sda1
error disk full on dev sda1
Warning: disk almost full on /dev/sda1
System boot sequence initiated.
system boot sequence completed.
```

Compile your code using `gcc /home/user/log_processor.c -o /home/user/log_processor` and run it to produce `/home/user/rolling_sim.csv`.