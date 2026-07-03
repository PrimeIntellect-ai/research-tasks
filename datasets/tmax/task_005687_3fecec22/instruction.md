You are a data scientist tasked with cleaning a messy dataset of international user reviews. You need to build a multi-stage bash pipeline using standard shell tools (`jq`, `sed`, `awk`, etc.) to process the data.

You have been provided with a raw JSONL file at `/home/user/raw_reviews.jsonl`. Each line is a JSON object with the following schema:
`{"id": integer, "user": "Name <email@domain.com>", "review": "Review text..."}`

The review text contains various languages, Unicode characters (including emojis), and occasionally Personally Identifiable Information (PII).

Write a shell script or pipeline that reads `/home/user/raw_reviews.jsonl` and generates a CSV file at `/home/user/cleaned_reviews.csv` with the following transformations:

1. **Extraction & Feature Engineering**: 
   - Parse the JSON fields.
   - Extract the email domain from the `user` field (e.g., if the user is "Alice <alice@example.com>", the domain is "example.com"). If no email is present, leave it empty.

2. **PII Anonymization**:
   - In both the `user` and `review` fields, replace any email addresses (matching `[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}`) with the literal string `[EMAIL]`.
   - In the `review` field, replace any phone numbers matching the exact pattern of 3 digits, a hyphen, and 4 digits (e.g., `123-4567`) with the literal string `[PHONE]`.

3. **Multi-language Text Processing**:
   - Calculate the word count of the *anonymized* review text. For this task, a "word" is defined as any sequence of non-whitespace characters (standard `awk '{print NF}'` or `wc -w` behavior).

4. **Output Generation**:
   - The output must be a valid CSV file located at `/home/user/cleaned_reviews.csv`.
   - The CSV must NOT have a header row.
   - The columns must be exactly in this order:
     `id,anonymized_user,anonymized_review,email_domain,review_word_count`
   - The `anonymized_user` and `anonymized_review` fields MUST be enclosed in double quotes.

Example Input Line:
`{"id": 1, "user": "Alice <alice@example.com>", "review": "Great product! Call 555-1234."}`

Expected Output Line:
`1,"Alice <[EMAIL]>","Great product! Call 555-[PHONE].","example.com",4`
*(Wait, 555-1234 matches 3 digits, hyphen, 4 digits. So "555-1234" becomes "[PHONE]".)*
Corrected Output Line:
`1,"Alice <[EMAIL]>","Great product! Call [PHONE].","example.com",4`

Ensure your pipeline handles multi-byte Unicode characters gracefully and relies only on standard Linux command-line tools.