You are a Machine Learning Engineer preparing a text dataset for a basic similarity search model. You have written a Go script to tokenize a corpus of text, compute Term Frequency (TF) vectors for each document, and find the two most similar documents using cosine similarity. 

However, you've hit a roadblock. Just like a misconfigured matplotlib backend that produces completely blank plots, your vectorization script is currently generating zero-vectors for all documents, resulting in a similarity score of `0.0000` across the board. 

Your task is to:
1. Identify and fix the bug in the data preparation script located at `/home/user/prep_data.go`. The bug is in how the term frequencies are calculated from the token counts.
2. Compile and run the script. It reads from `/home/user/corpus.txt`.
3. The script will automatically output the index of the two most similar documents and their cosine similarity score (formatted as `index1,index2,score`) to `/home/user/result.txt`. 

Make sure the output file `/home/user/result.txt` is successfully generated with the correct indices and a non-zero similarity score rounded to 4 decimal places.