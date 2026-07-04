You are given a CSV file containing synthetic word embeddings. Your task is to analyze these embeddings to find the most similar pair of distinct words based on cosine similarity.

The embeddings file is located at `/home/user/embeddings.csv`. 
It has the following format:
```csv
Word,v1,v2,v3,v4,v5
apple,0.5,0.1,0.2,-0.1,0.8
banana,0.4,0.15,0.25,-0.05,0.75
car,0.1,0.8,-0.5,0.4,0.1
truck,0.15,0.7,-0.4,0.5,0.05
dog,0.9,-0.2,0.1,0.1,0.1
cat,0.8,-0.1,0.2,0.0,0.2
```

Please perform the following steps:
1. Write a script in Python (or any other language you prefer) to read the CSV file.
2. Use linear algebra operations to compute the cosine similarity between all pairs of distinct words.
3. Identify the pair of distinct words that have the highest cosine similarity.
4. Write the names of these two words to a file named `/home/user/closest_pair.txt`. The words must be sorted alphabetically and separated by a single comma, with no spaces (e.g., `wordA,wordB`).

Do not include the similarity score in the output file, only the two words.