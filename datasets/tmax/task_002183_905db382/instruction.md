You are helping a data scientist clean and process a messy dataset of customer feedback surveys. You need to write a Python script that acts as a simple data pipeline to process this data. 

There is a raw dataset located at `/home/user/raw_surveys.csv` containing the following columns: `user_id`, `age`, `q1_response`, `q2_response`, and `q3_response`.

Please write a Python script at `/home/user/process_feedback.py` that performs the following pipeline steps sequentially:

1. **Wide-to-Long Reshaping:** Read the CSV. Melt the three response columns (`q1_response`, `q2_response`, `q3_response`) into two new columns: `question_id` (containing the column name, e.g., 'q1_response') and `raw_text` (containing the actual response text).
2. **Cleaning & Deduplication:** 
   - Drop any rows where `raw_text` is missing (NaN, null, or an empty string).
   - Deduplicate the data: if there are multiple rows with the same `user_id` AND `question_id`, keep only the first occurrence.
3. **Tokenization & Normalization:**
   - Create a new column called `normalized_text`.
   - To create this column from `raw_text`: convert the text to strictly lowercase, remove all punctuation (keep only alphanumeric characters and spaces), and replace any multiple consecutive spaces with a single space. Strip leading/trailing whitespace.
4. **Export:** Save the resulting DataFrame to `/home/user/final_surveys.csv`. It must contain exactly these columns: `user_id`, `age`, `question_id`, `normalized_text`. Sort the DataFrame ascendingly by `user_id`, then by `question_id`, before saving (do not include the index in the CSV).

**Logging Requirements:**
Your script must use Python's built-in `logging` module to write a log file to `/home/user/pipeline.log`. The logger should record the following exact messages at the `INFO` level:
- Upon starting: `Pipeline started`
- After reshaping: `Melted data: X rows` (where X is the integer number of rows)
- After cleaning and deduplication: `Cleaned data: Y rows` (where Y is the integer number of rows)
- Upon completion: `Pipeline completed`

Run your script to produce the final CSV and log file.