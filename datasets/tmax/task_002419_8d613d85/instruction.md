You are a data analyst tasked with processing a large stream of transaction logs. We have received a specification document as an image at `/app/schema_spec.png`. 

First, use OCR (e.g., `tesseract`) to read the text from `/app/schema_spec.png`. The document contains three critical pieces of information:
1. The exact subset of columns you need to extract from `/app/transactions.csv`.
2. The specific gap-filling rule for missing timestamps in the data stream.
3. The business logic for identifying "suspicious" transaction descriptions.

Your objectives:

1. **Streaming Data Pipeline:** 
   Write a script in a language of your choice that reads `/app/transactions.csv` in a streaming fashion (do not load the entire file into memory). Extract only the columns specified in the image. Apply the timestamp gap-filling rule exactly as described in the image. Write the processed records as a JSON Lines file to `/app/processed.jsonl`.

2. **Adversarial Filter Development:**
   Based on the business logic rules for "suspicious" descriptions found in the image, create an executable script at `/home/user/suspicious_filter`. 
   - The script must take a single file path as its first and only argument.
   - The file will contain a single transaction description as plain text.
   - The script must exit with code `0` if the description is clean/normal.
   - The script must exit with code `1` if the description is suspicious.
   
   Your filter will be tested against a hidden corpus of known-clean and known-suspicious descriptions.

Constraints:
- Ensure your data pipeline handles large files robustly.
- Make sure `/home/user/suspicious_filter` has executable permissions (`chmod +x`).
- Do not hardcode the logic before reading the image, as the exact rules are only found in `/app/schema_spec.png`.