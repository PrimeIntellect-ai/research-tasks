You are an expert data analyst. We have a set of customer interaction records, purchase histories, and a specific audio recording of a high-priority customer support call. Your goal is to analyze this call, extract the relevant entities, and construct a complex data pipeline to aggregate this customer's profile and graph of interactions.

Here are the requirements:

1. **Audio Processing**:
   An audio file of the VIP interaction is located at `/app/vip_call.wav`. You must transcribe this audio file. The transcription will contain a spoken Customer Reference ID (a string like "CUST-XXXX") and a mentioned Product Category.

2. **Data Ingestion & Aggregation**:
   You have the following data files:
   - `/app/data/customers.csv`: Contains customer metadata (`customer_id`, `name`, `region`).
   - `/app/data/interactions.csv`: Contains support tickets (`ticket_id`, `customer_id`, `issue_type`, `resolution_time`).
   - `/app/data/purchases.json`: A JSON Lines file containing NoSQL-style document records of purchases. Each line is a JSON object with a complex nested structure including `customer_ref`, `items` (array of objects), and `transaction_metadata`.

3. **Query Construction**:
   Write a Python script (`/home/user/build_profile.py`) that:
   - Takes the Customer Reference ID and Product Category extracted from the audio as parameterized inputs.
   - Joins the CSV data with the unpacked JSON document data.
   - Computes an aggregation pipeline: calculating the average `resolution_time` for this customer, the total amount spent on the mentioned Product Category, and a list of unique `issue_type`s they have experienced.
   - Output schema validation: The script must validate its final output against the following strict JSON structure and write the result to `/home/user/final_profile.json`:
     ```json
     {
       "customer_id": "string",
       "average_resolution_time": "float",
       "target_category_spend": "float",
       "unique_issues": ["string"]
     }
     ```

You may install any necessary Python libraries (e.g., `pandas`, `openai-whisper`, `pydantic`, `duckdb`) to accomplish this. Ensure your final output exactly matches the JSON schema and is saved to `/home/user/final_profile.json`.