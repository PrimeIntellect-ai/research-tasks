You are an automation specialist tasked with modernizing a data processing workflow for a multi-language customer support chat platform. We are preparing to bulk-export our raw chat logs into a new analytics database, but we must sanitize the data and standardize the time-series continuity.

Currently, we rely on a proprietary legacy engine to detect malicious inputs and PII. You will find this stripped binary at `/app/legacy_filter`. It is a command-line tool that takes a single text string as an argument and returns exit status `1` if the text contains prohibited content (PII, SQL injection payloads, or Unicode homoglyph spoofing), and exit status `0` if the text is clean. However, it is far too slow to be used in our bulk-export pipeline.

Your task is to reverse-engineer the rules implemented by `/app/legacy_filter` and write a high-performance C program that replicates its logic while simultaneously performing time-series gap-filling.

**Requirements:**
1. **Implementation:** Write a C program at `/home/user/pipeline.c` and compile it to `/home/user/pipeline`. 
2. **Execution Signature:** Your program must accept exactly two arguments: an input CSV file and an output CSV file.
   `./pipeline <input.csv> <output.csv>`
3. **Input Format:** The input is a UTF-8 CSV file with no header. The columns are `unix_timestamp,user_id,message`.
   Example: `1700000000,user_123,Hello there!`
4. **Processing Rules:**
   - **Filtering:** Evaluate the `message` column of each row. If the message violates the unknown rules of `/app/legacy_filter`, the row must be completely dropped from the output.
   - **Gap-Filling:** For the surviving (clean) rows, ensure a continuous timeline for each unique `user_id`. If there is a gap of *N* seconds between two consecutive messages from the same user, insert *N-1* rows for the missing seconds. The inserted rows must use the text `[GAP]` for the message.
5. **Output Format:** A bulk-import ready CSV matching the input format. 

You should use black-box testing against `/app/legacy_filter` to deduce its exact rules. We have provided some sample training logs in `/home/user/train/` to help you test your logic. Your final compiled binary must perfectly reject all "evil" messages and preserve all "clean" messages, exactly matching the legacy binary's classification, while inserting the correct gap-fill rows.