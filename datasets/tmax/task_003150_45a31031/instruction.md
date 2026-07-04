You are an AI assistant helping a data scientist clean a massive, multi-language dataset. We have a problem with datasets being poisoned by malicious Unicode (e.g., hidden control characters, directionality overrides) and garbage data (e.g., excessive punctuation from scraping errors). 

We have a vendored local package called `unicodenorm` located at `/app/unicodenorm-0.2.1`. However, it cannot be installed currently due to a deliberate configuration error in its package definition (a broken dependency version). 

Your task is to:
1. Fix the configuration of the `unicodenorm` package in `/app/unicodenorm-0.2.1` and install it in the local environment.
2. Write a Python script at `/home/user/cleaner.py` that reads a large text stream from `stdin` line by line and writes to `stdout`.
3. Your script must filter out (drop) any line that meets EITHER of the following conditions:
   a) `unicodenorm.is_malicious(line)` returns `True`.
   b) The line contains a high concentration of punctuation. Specifically, compute a rolling statistic: for any window of 20 consecutive characters in the line, if the number of punctuation and symbol characters (Unicode categories `P*` and `S*`) strictly exceeds 10, the line must be dropped. If a line is shorter than 20 characters, evaluate the ratio on the whole line (drop if punctuation/symbols > 50% of the line length).
4. Lines that do not trigger the above conditions must be written to `stdout` exactly as they appeared in `stdin` (preserving the original newline characters).
5. The script must be memory-efficient (capable of streaming gigabytes of data without loading everything into RAM at once).

Your solution will be tested against two sets of files:
- A "clean" corpus of multi-language text (which your script must preserve 100%).
- An "evil" corpus containing malicious Unicode and heavily corrupted scraped lines (which your script must reject 100%).

Ensure your script is executable and handles standard input/output properly. You can test your logic by creating your own small text files.