You are a data engineer working on an ETL pipeline that merges legacy user profiles with a newly imported dataset. 

You have been given two JSON-Lines files:
1. `/home/user/legacy.jsonl`
2. `/home/user/new.jsonl`

Due to a bug in the legacy system's export tool, the `bio` field in `legacy.jsonl` contains heavily double-escaped unicode sequences (e.g., `\\u00f1` instead of the actual `ñ` character). The `new.jsonl` file, however, is correctly encoded in UTF-8.

Your task is to write and execute a Python script that does the following:
1. Parse both JSONL files.
2. Clean the `bio` field in the legacy data by properly decoding the double-escaped unicode sequences into standard UTF-8 strings.
3. Perform an inner join of the two datasets on the `user_id` field.
4. For each joined record, compute the string similarity ratio between the cleaned legacy `bio` and the new `bio` using Python's built-in `difflib.SequenceMatcher(None, string1, string2).ratio()`.
5. We consider a profile update anomalous if the similarity ratio between the old and new bio is strictly less than `0.75`. 
6. Extract the `user_id`s of all anomalous records and save them to `/home/user/anomalies.txt`, writing one `user_id` per line, sorted in ascending numerical order.

Requirements:
- Only use Python standard libraries (e.g., `json`, `difflib`, `codecs`).
- Do not use external libraries like `pandas`.
- Make sure `/home/user/anomalies.txt` is created exactly as requested.