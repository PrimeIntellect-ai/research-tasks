You are a data engineer tasked with building a robust ETL pipeline to process customer feedback from multiple upstream systems.

Your goal is to write a bash script at `/home/user/run_pipeline.sh` that, when executed, orchestrates the entire process: setting up the environment, executing the ETL steps via Python, and producing a final stratified sample.

The input data is located in `/home/user/raw_data/` and comes in three different formats, each with slightly different schemas:
1. `feedbacks.jsonl`: Contains `{"uid": <int>, "review_text": "<string>", "mood": "<string>"}`
2. `comments.csv`: Contains columns `row_id`, `user_comment`, `label`
3. `responses.xml`: Contains `<data><entry><id><int></id><content><string></content><feeling><string></feeling></entry></data>`

Pipeline Requirements:
1. **Extract**: Read all three files.
2. **Transform**:
   - Normalize the schema for all records to have exactly four columns: `id` (integer), `text` (string), `sentiment` (string, which maps to mood/label/feeling), and `source` (string, the name of the source file, e.g., "feedbacks.jsonl").
   - Clean the `text` field: Convert all characters to lowercase and remove all characters EXCEPT alphanumeric characters (a-z, 0-9) and spaces.
3. **Sample and Stratify**: 
   - We need a strictly deterministic stratified sample for downstream annotation.
   - For EACH unique `sentiment` category (which will be 'positive', 'neutral', and 'negative'), select exactly 3 records.
   - To ensure deterministic output, select the 3 records with the *lowest numerical `id`* within each sentiment category.
4. **Load**:
   - Save the final 9-record dataset as a Parquet file at `/home/user/processed/stratified_sample.parquet`.
   - Ensure the Parquet file maintains the standard schema: `id`, `text`, `sentiment`, `source`.

Requirements for your solution:
- Write the orchestrator bash script at `/home/user/run_pipeline.sh`. Make it executable.
- The bash script should install any required Python packages (e.g., pandas, pyarrow, lxml) via pip, and then execute the Python pipeline.
- All Python code should be written to `/home/user/etl_pipeline.py` and called by the bash script.
- Create the `/home/user/processed/` directory if it does not exist.

Ensure your pipeline handles the text cleaning and sorting correctly.