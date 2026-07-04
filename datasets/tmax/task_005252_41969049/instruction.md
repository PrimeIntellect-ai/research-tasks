You are a data analyst preparing a dataset for a machine learning model. You have been given a messy CSV file of product reviews located at `/home/user/raw_data.csv`. 

Your task is to write a Go program at `/home/user/process.go` that processes this CSV file and saves the result to `/home/user/clean_data.csv`. You must enforce a strict schema, engineer a new feature, and tokenize the text data.

Here are the requirements for the processing:
1. **Schema Enforcement**: 
   - Read the input CSV which has columns: `id`, `age`, `review`.
   - Drop any rows where `id` is not a valid standard UUID (format: 8-4-4-4-12 hexadecimal characters).
   - Drop any rows where `age` is not a valid integer or is outside the range 18 to 100 (inclusive).

2. **Feature Engineering**:
   - Create a new column called `age_group` based on the `age`:
     - `youth` for ages 18 to 29 (inclusive).
     - `adult` for ages 30 to 59 (inclusive).
     - `senior` for ages 60 and above.

3. **Tokenization**:
   - Process the `review` column to create a `review_tokens` column.
   - Convert the text to lowercase.
   - Remove all commas `,` and periods `.`.
   - Split the text into individual words (tokens) by whitespace.
   - Join the resulting tokens using a pipe character `|`. (e.g., "Good product, nice." becomes "good|product|nice")

4. **Output Format**:
   - The output file `/home/user/clean_data.csv` must include exactly these columns in order: `id,age,age_group,review_tokens`.
   - The first row of the output file must be the header.

Once your Go script is written, run it to generate `/home/user/clean_data.csv`.