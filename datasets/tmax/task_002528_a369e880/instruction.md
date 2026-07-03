You are a data engineer building an ETL pipeline to process a large corpus of multi-lingual chat logs. The raw data is located at `/home/user/raw_logs.jsonl`. Each line is a JSON object with the following schema:
`{"id": int, "timestamp": string_or_float, "lang": string, "msg": string}`

We need to perform data normalization, tokenization, timestamp alignment, and stratified sampling.

Your tasks are:
1. **Fix and Install the Vendored Tokenizer**:
   We have a proprietary C-extension tokenizer vendored at `/app/fast_log_tokenizer-0.1`. However, it currently fails to build/install due to a small misconfiguration in its build files. Fix the package and install it in the environment. Once installed, it provides a module `fast_log_tokenizer` with a `tokenize(text: str) -> list[str]` function.
   
2. **Process the Logs**:
   Write a Python script that reads `/home/user/raw_logs.jsonl` and processes each record:
   - **Timestamp Alignment**: The `timestamp` field in the raw data is extremely messy (a mix of epoch seconds, epoch milliseconds, and various string formats like 'YYYY/MM/DD HH:MM:SS'). Parse them and convert them all to standard ISO 8601 UTC strings formatted exactly as `YYYY-MM-DDTHH:MM:SSZ`.
   - **Tokenization**: Use the installed `fast_log_tokenizer.tokenize()` to tokenize the `msg` field. 
   - **Normalization**: Convert all tokens to lowercase and remove any tokens that consist solely of whitespace or are empty. Replace the original `msg` string with a new field `tokens` containing this list of normalized strings.
   
3. **Stratified Sampling**:
   We need a representative sample of exactly 1,000 records for downstream human review. You must perform stratified sampling based on the `lang` field. The distribution (proportions) of the `lang` field in your 1000-record sample must closely match the distribution in the entire raw dataset.

4. **Output**:
   Save your final 1000 sampled and processed records to `/home/user/processed_logs.jsonl`. Each line must be a valid JSON object matching this schema:
   `{"id": int, "timestamp": string, "lang": string, "tokens": list[string]}`

You may use any standard Python libraries as well as `pandas` or `numpy` if desired. The goal is to maximize the accuracy of the timestamps and the correct distribution of languages.