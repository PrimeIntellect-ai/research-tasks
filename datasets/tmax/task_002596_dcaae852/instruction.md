You are an ML engineer preparing text data for a semantic search model. You need to write a pure Bash script to tokenize a corpus and perform a simple keyword-based similarity search to extract relevant training examples.

Your task is to create a Bash script at `/home/user/extract_similar.sh` that does the following:
1. Takes two arguments: an input text file path and a target phrase (a string of words).
2. For every line in the input file, "tokenizes" the line by converting it to lowercase and removing all characters except letters (a-z) and spaces. Multiple spaces should be collapsed to a single space.
3. Tokenizes the target phrase in the exact same way.
4. Calculates a "similarity score" for each line, defined as the absolute number of unique words from the target phrase that appear in the tokenized line.
5. Sorts the lines based on this similarity score in descending order. If there is a tie, preserve the original order of appearance in the file.
6. Writes the top 3 original, unmodified lines (from the input file) to `/home/user/top_matches.txt`.

Before writing the script, create a test corpus at `/home/user/corpus.txt` with the following 5 lines exactly:
```
Deploying a machine learning model to production is hard.
Deep learning models require a lot of data.
We are learning how to deploy deep neural networks.
The deployment of a deep learning model is a critical step.
Data science involves analyzing data to find patterns.
```

Run your script using:
`bash /home/user/extract_similar.sh /home/user/corpus.txt "deployment of a deep learning model"`

Make sure `/home/user/top_matches.txt` is generated and contains exactly the 3 best matching lines, separated by newlines.