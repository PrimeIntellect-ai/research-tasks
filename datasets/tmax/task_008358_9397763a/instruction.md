You are a researcher organizing a text dataset for a downstream machine learning model. You want to measure the Out-Of-Vocabulary (OOV) rate on your test set to ensure the test data doesn't contain too many unseen tokens compared to the training data.

However, you want to strictly prevent data leakage: the vocabulary must be built *only* from the training set, and must only include tokens that appear multiple times. 

You have two files: `/home/user/train.tsv` and `/home/user/test.tsv`. 
Both files are expected to follow this schema: `<integer_id>\t<text>`.

Using **Bash and standard Unix utilities (like awk, sed, grep, bc)**, write a script or execute commands to perform the following:

**1. Schema Enforcement & Tokenization:**
For both files, ignore any lines that do not strictly match the schema (an integer ID, a single tab character, and text). 
To tokenize the text: 
- Convert all text to lowercase.
- Replace all non-alphanumeric characters (anything not `a-z` or `0-9`) with a single space.
- Split into tokens by whitespace.

**2. Vocabulary Construction (Train only):**
Build a vocabulary from the valid lines in `train.tsv`. A token is included in the vocabulary *only* if it appears **2 or more times** across the entire tokenized training set.

**3. OOV Inference (Test):**
For each valid line in `test.tsv`, calculate its OOV rate:
- Let $W$ be the total number of tokens in the line.
- Let $U$ be the number of tokens in the line that are **not** in the vocabulary.
- The OOV rate $r = U / W$. (If a line has 0 tokens, $r = 0$).

**4. Hypothesis Testing / Statistics:**
Calculate the sample mean ($\mu$) and the sample standard deviation ($s$) of the OOV rates across all valid test lines.
Compute the 95% Confidence Interval margin of error for the mean using the formula:
$E = 1.96 \times \frac{s}{\sqrt{N}}$
(where $N$ is the number of valid test lines).

Write exactly one line to `/home/user/oov_stats.txt` containing the mean and the margin of error, separated by a comma, both rounded to exactly 4 decimal places.
Format: `Mean,MarginOfError`
Example: `0.4500,0.1234`