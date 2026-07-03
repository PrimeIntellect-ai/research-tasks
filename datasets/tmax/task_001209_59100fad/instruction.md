You are a performance engineer tasked with debugging a financial data pipeline. We are noticing that some transactions are suffering from unacceptable precision loss as they pass through our microservices (gateway, processor, and settlement), but the logs are heavily interleaved and out of order.

We need a detection script to automatically flag transactions that exceed our precision loss tolerance. The exact tolerance threshold was documented in a system configuration screenshot saved at `/app/threshold.png`. You will need to extract the `MAX_ALLOWED_LOSS` value from this image.

Write a Python script at `/home/user/detect.py` that takes a single log file path as its command-line argument.
Each log file contains a sequence of JSON-formatted log entries, but they are completely out of order. Your script must:
1. Parse the JSON lines and reconstruct the timeline for the transaction based on the `tx_id` (there will be exactly one `tx_id` per file).
2. Locate the initial event from the `gateway` service, which contains an `amount` field (a string representing a high-precision float).
3. Locate the final event from the `settlement` service, which contains a `final_amount` field (a floating-point number).
4. Calculate the precision loss as the absolute difference between the gateway's `amount` and the settlement's `final_amount`.
5. Compare the precision loss against the `MAX_ALLOWED_LOSS` extracted from the image.

**Exit Code Requirements:**
- If the precision loss is strictly greater than the `MAX_ALLOWED_LOSS`, the transaction is considered corrupted. Your script MUST exit with status code `1` (reject).
- If the precision loss is less than or equal to the `MAX_ALLOWED_LOSS`, the transaction is acceptable. Your script MUST exit with status code `0` (accept).

You may use any tools installed on the system (e.g., `tesseract` for OCR) to read the image, but the final logic must be encapsulated in your `/home/user/detect.py` script.