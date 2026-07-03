You are a monitoring specialist tasked with setting up a critical alert parsing pipeline for our network operations center. 

We receive raw alert logs in JSON format, but they need to be normalized and filtered before being sent to our mailing list server. The exact formatting rules and severity thresholds have been provided by the senior network engineer in an image file located at `/app/alert_rules.png`.

Your task is to:
1. Extract the parsing and formatting rules from the image at `/app/alert_rules.png`. You may use tools like `tesseract` to read the image text.
2. Write a Python script at `/home/user/alert_parser.py` that reads raw logs from standard input (one JSON object per line) and writes the formatted alerts to standard output (one per line).
3. The input JSON objects will always contain the keys: `timestamp` (integer), `severity` (integer), `source` (string), and `message` (string).
4. If a line cannot be parsed as valid JSON or is missing any of these keys, the script should output the exact string `INVALID_LOG` for that line.
5. Apply the severity thresholds and string formatting exactly as specified in the image.

Your script must be robust and perfectly match the expected output format, as it will be rigorously verified against a reference oracle implementation using a fuzzer.