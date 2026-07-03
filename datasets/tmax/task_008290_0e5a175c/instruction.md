Hey there,

I'm working on a new analytics ingestion feature for our web application, but I've hit a wall with our Go processing pipeline. 

Our CI test suite is failing because the Go processor I wrote works fine for small sequential unit tests, but when I tried to scale it up using goroutines for bulk webhook fixtures, the output either gets out of order or drops records. 

Here is the situation:
We have a batch fixture of webhook payloads located at `/home/user/data/webhooks.jsonl`. 
Each line is a JSON object representing a webhook, containing:
- `id` (integer)
- `encoded_data` (string): The raw webhook payload encoded in standard Base64.
- `checksum` (unsigned 32-bit integer): The expected IEEE CRC32 checksum of the **decoded** payload.

I need you to write a Go program at `/home/user/workspace/filter.go` that does the following:
1. Reads `/home/user/data/webhooks.jsonl` line by line.
2. Parses the JSON.
3. Decodes the `encoded_data` using standard Base64.
4. Calculates the IEEE CRC32 checksum of the decoded byte array.
5. Checks if the calculated checksum matches the `checksum` field in the JSON.
6. Writes the **exact original JSON string** (with its trailing newline) of each *valid* webhook to `/home/user/workspace/valid_webhooks.jsonl`.

**Crucial Constraints:**
- Because checksum calculation can be CPU-intensive at scale, you **must** perform the validation steps (decoding and CRC32 calculation) concurrently using goroutines.
- The output in `/home/user/workspace/valid_webhooks.jsonl` **must maintain the exact same relative order** as the input file. You cannot just output lines as soon as the goroutine finishes, because they will complete out of order.

Please write the script, build it, and run it to produce the `/home/user/workspace/valid_webhooks.jsonl` file. Our automated system will check this output file to verify your fix. 

Thanks!