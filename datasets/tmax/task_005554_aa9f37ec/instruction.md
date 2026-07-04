You are a data analyst troubleshooting a set of noisy log files from a legacy system. 

Your task is to process a CSV file containing log messages, remove exact duplicates (regardless of case or leading/trailing whitespace), compute a rolling similarity metric between consecutive unique logs, and output the results to a JSON file.

Here are the specific requirements:
1. **Input File**: Read the file `/home/user/sensor_logs.csv`. It contains two columns: `LogID` and `Message`.
2. **Character Encoding**: The CSV file is encoded in `cp1252`. You must read it correctly.
3. **Hash-Based Deduplication**: 
   - Normalize the `Message` by stripping leading/trailing whitespace and converting it to entirely lowercase.
   - Compute the SHA-256 hash of the UTF-8 encoded string of this normalized message.
   - Keep only the *first* occurrence of each hash. Discard any subsequent rows that result in a hash you have already seen.
4. **Windowed Similarity Computation**:
   - Iterate through the deduplicated rows in their original order.
   - For each row, calculate the string similarity ratio between its normalized message and the *immediately preceding* deduplicated row's normalized message.
   - Use Python's built-in `difflib.SequenceMatcher(None, prev_msg, curr_msg).ratio()` for the similarity.
   - For the very first deduplicated row, the similarity score should be exactly `0.0`.
5. **Output**: Write the results to `/home/user/processed_logs.json`.
   - The file must contain a JSON array of objects.
   - Each object must have exactly three keys: `LogID` (as an integer), `Message` (the *original* un-normalized string from the CSV), and `Similarity` (the float similarity score rounded to exactly 4 decimal places).

Write a Python script to perform this data pipeline and execute it to generate the output file.