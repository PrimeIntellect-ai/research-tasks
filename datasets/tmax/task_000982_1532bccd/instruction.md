You are a data analyst tasked with building a reproducible text processing and statistical analysis pipeline using Bash and standard Linux command-line tools.

You have been provided with two files:
1. `/home/user/reviews.csv` - A CSV file containing customer reviews. It has a header and three columns: `id,rating,text`. The `rating` is an integer from 1 to 5.
2. `/home/user/stopwords.txt` - A text file containing stop words (one per line).

Write a Bash script located at `/home/user/pipeline.sh` that performs the following steps when executed. Your script must be strictly reproducible.

**Step 1: Tokenization & Dimensionality Reduction (Feature Selection)**
Parse the `text` column of the entire `reviews.csv` file to find the 3 most frequent valid words across the dataset. 
- Tokenization rules: Convert all text to lowercase. Replace any non-alphabetic characters (anything not `a-z`) with a space. Split the text into words by whitespace.
- A valid word must be at least 3 characters long and must NOT appear in `/home/user/stopwords.txt`.
- These 3 words represent our reduced feature space. In case of a frequency tie, sort alphabetically and pick the first ones.

**Step 2: Bootstrap Sampling**
Generate 3 bootstrap samples (sampling with replacement) of the original `reviews.csv` (excluding the header). Each bootstrap sample must contain the same number of rows as the original dataset.
- To ensure pipeline reproducibility, you MUST use the `shuf` command to generate the bootstrap samples.
- Use the provided random source file `/home/user/random_seed.dat` (which already exists) for `shuf` to ensure deterministic output. Use the exact arguments: `shuf -r -n <num_rows> --random-source=/home/user/random_seed.dat`.
- Note: Run the `shuf` command exactly 3 times in a row, generating sample 1, then sample 2, then sample 3. Do not include the CSV header in the sampled rows.

**Step 3: Average Target Calculation (Regression Proxy)**
For each of the 3 chosen feature words, and for each of the 3 bootstrap samples, calculate the mean `rating` of the reviews whose tokenized text contains that exact word. 

**Output Generation**
Your script must output a final report to `/home/user/report.csv` with the following format (including header):
```csv
Sample_ID,Word,Average_Rating
```
- `Sample_ID` should be 1, 2, and 3.
- `Word` should be the feature word.
- `Average_Rating` should be rounded to exactly 2 decimal places (e.g., `3.50`).
- Sort the output file first by `Sample_ID` (ascending), then by `Word` (alphabetically).

Ensure your script has executable permissions and runs cleanly without user interaction. Execute the script to produce `/home/user/report.csv`.