You are a data analyst tasked with processing a dataset of product reviews. You need to build a simple bash-based ETL pipeline that reads the data, tokenizes the text, performs dimensionality reduction by selecting the most frequent words (a basic Bag-of-Words feature extraction), and outputs a feature matrix.

You are provided with two files:
1. `/home/user/reviews.csv`: A CSV file with a header row `id,rating,review_text`.
2. `/home/user/stopwords.txt`: A text file containing one stop word per line.

Your objective is to create a shell script or run bash commands to generate a new CSV file at `/home/user/bow_features.csv` according to the following rules:

**Step 1: Tokenization and Cleaning**
Extract the `review_text` for each row. Convert all characters to lowercase. Replace any character that is NOT a lowercase letter (`a-z`) or a space with a space. Split the text into individual words based on whitespace.

**Step 2: Stopword Removal & Feature Selection (Dimensionality Reduction)**
Calculate the global frequency of each valid word across all reviews. Completely ignore/remove any words that exactly match a word in `/home/user/stopwords.txt`. 
Identify the top 3 most frequent remaining words in the entire dataset. If there is a tie in frequencies, resolve it by sorting the tied words alphabetically.
Sort these top 3 words alphabetically to form your fixed feature dimensions.

**Step 3: Feature Matrix Generation**
Generate a file named `/home/user/bow_features.csv`. 
The first row must be the header: `id,word1,word2,word3` (where word1, word2, and word3 are the alphabetically sorted top 3 words you found).
For each `id` in the original dataset (excluding the header), output a row containing the `id`, followed by the exact count of times each of the 3 feature words appeared in that specific review's cleaned text. Use commas to separate the values.

Requirements:
- Ensure the output strictly follows the CSV format without spaces after commas.
- Your solution should primarily rely on Bash utilities (`awk`, `sed`, `grep`, `tr`, `sort`, `uniq`, etc.).