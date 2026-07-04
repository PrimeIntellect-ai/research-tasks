You are a localization engineer managing a pipeline of newly crowdsourced string translations. You need to process a dataset of proposed translations, evaluate their structural similarity to the source text using our proprietary oracle tool, and expose the accepted translations via a simple internal TCP service for our integration tests.

You are restricted to using Bash and standard Linux shell utilities (awk, sed, grep, socat, nc, coreutils, etc.). Do not use Python, Perl, Ruby, or other scripting languages for the logic.

**Your Setup & Inputs:**
1. A dataset at `/home/user/raw_translations.tsv` containing four tab-separated columns: `ID`, `LangCode`, `SourceText`, and `ProposedText`.
2. A proprietary, compiled binary at `/app/tqs` (Translation Quality Scorer). It is a stripped binary that takes two string arguments and prints a floating-point similarity score to standard output. Usage: `/app/tqs "string 1" "string 2"`.

**Step 1: Tokenization and Normalization**
For each row in the dataset (skipping the header if any), you must normalize both the `SourceText` and `ProposedText`.
Normalization rules:
- Convert all characters to lowercase.
- Remove all characters except alphanumeric characters (a-z, 0-9) and spaces.

**Step 2: Distance Computation and Quality Gate**
Compute the similarity score between the *normalized* `SourceText` and the *normalized* `ProposedText` using the `/app/tqs` binary. 
Filter the dataset to only retain translations that achieve a score strictly greater than or equal to `0.50`.

**Step 3: Data Sampling and Stratification**
From the translations that passed the quality gate, stratify by `LangCode`. For each language code, keep exactly the top 2 translations with the highest scores. If there is a tie in scores, sort by `ID` in ascending order to break the tie.

**Step 4: TCP Service Integration**
Create and run a pure Bash-based server script at `/home/user/serve.sh` that listens for raw TCP connections on `127.0.0.1:9090`. 
- Protocol: The server must accept a single line of text per connection.
- Request format: `FETCH <ID>` (e.g., `FETCH 104`)
- Response format: If the `ID` is in your final stratified set, respond with the *original, un-normalized* `ProposedText` followed by a newline (`\n`). 
- Error handling: If the ID is not found, or the command is invalid, respond with `ERROR\n`.
- The server must handle multiple sequential requests without crashing (it does not need to handle concurrent requests). Use `socat` or `nc` in a loop.

Start your server in the background so it remains running when you complete your interactions. Ensure the final processed dataset is also saved to `/home/user/accepted_translations.tsv` for reference.