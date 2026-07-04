You are an MLOps engineer tasked with building a secure, high-performance ETL pipeline for text data. We need to tokenize incoming documents and filter out obfuscated "adversarial" texts that attempt to bypass our data processing pipelines. 

To accomplish this, you must use our internal fast tokenization library. However, the repository we cloned seems to have a broken configuration.

Your objectives:
1. **Fix and Install the Vendored Package:**
   We have vendored our internal tokenizer at `/app/vendored/tok_speed`. The installation is currently failing due to a typo in the package configuration file. Fix the setup file and install the package so that it can be imported (e.g., `import tok_speed`). The library exposes a `tokenize(text)` function that returns a list of strings.

2. **Build the ETL Pipeline Script:**
   Create a CLI script at `/home/user/pipeline.py` that takes two arguments: an input file path and an output file path.
   Usage: `python /home/user/pipeline.py <input_file> <output_file>` (or equivalent in your language of choice).
   
   The script must read the input text, tokenize it using `tok_speed.tokenize(text)`, and then apply a statistical filter to detect adversarial obfuscation.

3. **Implement the Statistical Filter (Sampling and Bootstrap):**
   Adversarial documents in our system typically contain tokens with abnormal lengths. However, simple means are skewed by outliers. You must use a bootstrap method to evaluate the token lengths:
   - Calculate the lengths of all tokens in the document. Let `N` be the total number of tokens.
   - Generate `1000` independent bootstrap samples of these lengths. Each bootstrap sample must be drawn *with replacement* from the document's token lengths, and each sample must be of size `N`.
   - Calculate the **median** token length for each of the 1000 bootstrap samples.
   - Calculate the **95th percentile** of these 1000 medians.
   - **Filter Condition:** If the 95th percentile of the bootstrap medians is `>= 7.0`, the script must classify the document as adversarial/evil.

4. **Integration and Benchmarking:**
   - **If Adversarial (Rejected):** The script must immediately exit with status code `1`. Do not create or write to the output file.
   - **If Clean (Accepted):** The script must write the tokens as a space-separated string to the `<output_file>`. 
   - **Benchmarking:** Every time a clean document is successfully processed, the script must measure the total wall-clock time taken for *both the tokenization and the bootstrap evaluation* phases. Append a single line with the duration in seconds (as a float) to `/home/user/benchmark_log.txt`. Finally, exit with status code `0`.

We have provided a set of clean documents in `/app/data/clean/` and a set of adversarial documents in `/app/data/evil/`. Your pipeline must perfectly separate them.