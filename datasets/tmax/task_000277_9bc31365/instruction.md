You are a data scientist tasked with preparing a text dataset and creating reproducible bootstrap samples using only Bash and standard UNIX utilities (like `awk`, `tr`, `sed`, `grep`). 

You have been provided with a raw text file at `/home/user/raw_corpus.txt`.

Your goal is to build a robust shell-based data processing pipeline that tokenizes the text, followed by a reproducible bootstrap sampling step.

Please complete the following steps:

1. **Tokenization & Data Cleaning Pipeline**
   Create a cleaned token list from `/home/user/raw_corpus.txt` and save it to `/home/user/tokens.txt`.
   The cleaning pipeline must do the following in order:
   - Convert all text to lowercase.
   - Replace any non-alphanumeric character (anything that is not a-z, 0-9) with a space.
   - Split the text by spaces so that there is exactly one token (word) per line.
   - Remove any empty or entirely whitespace lines.

2. **Reproducible Bootstrap Sampling**
   Write a Bash script at `/home/user/bootstrap.sh` that takes exactly three arguments in this order:
   `./bootstrap.sh <input_file> <sample_size> <seed>`
   
   The script must randomly sample lines from the `<input_file>` **with replacement** to produce exactly `<sample_size>` lines of output to `stdout`. 
   To ensure pipeline reproducibility, you must use GNU `awk`'s random number generator initialized with the provided `<seed>` (e.g., using `srand(seed)` and `rand()`).
   *Note: Ensure your awk sampling logic correctly targets indices from 1 to the total number of lines.*

3. **Generate Samples**
   Using your `/home/user/bootstrap.sh` script, generate three bootstrap samples from `/home/user/tokens.txt`. Each sample must be of size `N=1000`.
   - For seed `42`, save to `/home/user/sample_42.txt`
   - For seed `123`, save to `/home/user/sample_123.txt`
   - For seed `999`, save to `/home/user/sample_999.txt`

4. **Verification Log**
   Compute the SHA-256 checksums of your three generated sample files.
   Run `sha256sum /home/user/sample_42.txt /home/user/sample_123.txt /home/user/sample_999.txt > /home/user/checksums.txt`.

Ensure all files are created exactly at the specified paths.