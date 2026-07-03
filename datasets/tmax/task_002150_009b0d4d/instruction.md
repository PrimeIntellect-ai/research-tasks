You are tasked with writing a high-performance configuration state tracker in C. We receive streams of configuration updates from legacy systems, but the documentation for the specific keys we need to extract and the required normalization prefix was lost in a system migration. Fortunately, a scanned copy of the original specification memo has been recovered.

Your objectives:
1. Examine the image located at `/app/memo.png` (you may need to install and use OCR tools like `tesseract-ocr` to read it). The memo contains:
   - A mandatory prefix string that must be prepended to all output keys.
   - A specific list of exactly four configuration keys that we care about tracking.
   - A special validation rule for one of the numerical keys.

2. Write a C program at `/home/user/config_tracker.c` and compile it to `/home/user/config_tracker`. The program must act as a stream processor:
   - It should read line-by-line from `standard input` until EOF.
   - Each line represents a configuration update in the format: `[whitespace]Key[whitespace]:[whitespace]Value[whitespace]`
   - **Key Normalization**: Keys are case-insensitive and should be tracked in lowercase. Ignore any keys not explicitly listed in the memo. 
   - **Value Decoding**: The values are URL-encoded (e.g., `%20` for space, `%2D` for `-`, `%3A` for `:`). Your program must decode these URL-encoded values back to standard ASCII characters.
   - **Deduplication**: If a tracked key appears multiple times in the stream, the *last* valid value read should overwrite previous ones.
   - **Validation**: Apply any specific validation/clamping rules mentioned in the memo to the decoded values.
   - **Output**: Once EOF is reached, print the final tracked state to `standard output`. Only print keys that were present in the input stream. Print them in alphabetical order based on the key name. The output format must be: `PREFIX-key=decoded_value\n` (where PREFIX is the exact prefix from the memo).

Ensure your compiled executable is located at `/home/user/config_tracker` and is executable. It will be rigorously tested against thousands of randomized configuration streams to ensure perfect compliance with the parsing, decoding, and tracking rules.