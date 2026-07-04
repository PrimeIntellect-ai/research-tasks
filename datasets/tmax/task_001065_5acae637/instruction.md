You are an integration developer analyzing API test results. We have received an image containing the latest evaluation specification from the architecture team, located at `/app/api_spec.png`. 

Your task is to:
1. Use optical character recognition (OCR) or a vision script to extract the text from `/app/api_spec.png`. The image contains a minimum required semantic version and a mathematical scoring formula involving variables `A`, `B`, and `C`.
2. Read the API test results from `/app/responses.jsonl`. Each line is a JSON object with two keys: `version` (a semantic version string) and `payload` (a base64-encoded JSON string).
3. Filter the results to only include those where the `version` is strictly greater than or equal to the minimum required semantic version extracted from the image. Note that standard semantic versioning rules apply (e.g., 2.2.0 > 2.1.5).
4. For each valid record, decode the base64 `payload` to retrieve a JSON object containing the numeric variables `A`, `B`, and `C`.
5. Parse and evaluate the extracted mathematical formula for each valid record.
6. Calculate the average (mean) score across all valid records.
7. Write ONLY the final average score as a floating-point number to `/home/user/result.txt`.

Example expected format of `/home/user/result.txt`:
45.25