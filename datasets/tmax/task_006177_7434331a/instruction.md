You are an AI assistant helping a researcher organize and analyze a large dataset of raw text logs. 

The researcher has a collection of text files in `/home/user/dataset/`. They were trying to write a script to compute token frequencies to feed into a visualization tool, but their current script keeps crashing with out-of-memory errors because it tries to load all files into a single array at once. Furthermore, their tokenization logic was leaving trailing punctuation, causing the downstream visualization script to produce blank plots due to unrecognized categories.

Your task is to properly tokenize the dataset and find the most frequent words. You can use any programming language (Python, Bash, etc.) to accomplish this, but you must handle the data efficiently.

Here are the strict tokenization and processing rules you must follow:
1. Process all `.txt` files in `/home/user/dataset/`.
2. Convert all text to lowercase.
3. Replace all non-alphanumeric characters (anything that is not `a-z` or `0-9`) with a single space.
4. Split the text into individual tokens based on whitespace.
5. Discard any tokens that are less than 4 characters long.
6. Count the frequency of each remaining token across the entire dataset.

Calculate the top 10 most frequent tokens. If there are ties in the frequency count, sort the tied tokens alphabetically in ascending order.

Save the final top 10 list to `/home/user/top_tokens.txt`.
The file must contain exactly 10 lines. Each line must be formatted as `<count> <token>` (e.g., `450 quantum`), with a single space separating the count and the token. Do not include any headers or extra whitespace.