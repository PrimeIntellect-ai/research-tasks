You are a release manager preparing for the deployment of a new microservice. Before releasing, you must ensure that staging API logs do not leak sensitive credentials. You have an export of gRPC payload logs in JSON format, a Protobuf schema, and a list of compromised security tokens. 

Your task is to write a Python application that processes these logs, redacting any compromised tokens efficiently using a custom data structure.

Here are the requirements:
1. **Setup**: Work in `/home/user/workspace`. Ensure you install the required Protobuf compiler tools (`grpcio-tools`).
2. **Compile Protobuf**: You are provided with a `/home/user/workspace/schema.proto` file. Compile it to Python code in the same directory.
3. **Custom Data Structure**: Inside a script named `/home/user/workspace/redactor.py`, implement a custom Prefix Tree (Trie) class named `TokenTrie`. This class must have an `add_token(token)` method and a `redact(text)` method. The `redact` method must efficiently scan the input string and replace any instances of the stored tokens with the exact string `[REDACTED]`. Do not just use a list of `str.replace` calls; you must implement and use the Trie logic for the search and replace.
4. **Structured Data Parsing**: 
   - Read the sensitive tokens from `/home/user/workspace/tokens.txt` (one token per line) and load them into your `TokenTrie`.
   - Read the logs from `/home/user/workspace/payloads.jsonl`. Each line is a JSON object representing the `TransactionLog` message defined in `schema.proto`.
   - For each JSON object, extract the fields. For any field that is typed as a `string` in the Protobuf schema, apply the `TokenTrie.redact()` method to its value. Non-string fields (like integers) should be left alone.
5. **Output**:
   - Write the sanitized JSON objects to `/home/user/workspace/redacted.jsonl`. Each line must be a valid JSON object.
   - Keep a count of the total number of times a token was found and replaced across all logs. Write this summary as a JSON object to `/home/user/workspace/summary.json` in the format: `{"total_redactions": N}`.

Once you have written `redactor.py`, execute it to generate the `redacted.jsonl` and `summary.json` files.