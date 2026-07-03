You are assisting a researcher organizing a massive dataset of cross-representational data (mapping relational tables and document stores into a unified graph format). We are building an automated pipeline to execute complex joins, subqueries, and pagination across these representations.

However, we are receiving dirty and potentially malicious query configurations from external sources. The principal investigator left an audio recording detailing the strict validation rules for the queries. 

Your task:
1. Listen to / transcribe the audio file located at `/app/audio/directive.wav` to discover the exact filtering rules.
2. Create a Rust CLI application in `/home/user/query_sanitizer/` that acts as a filter for our graph query JSON configurations.
3. The Rust application must take a single file path as a command-line argument.
   Example: `cargo run --release -- /path/to/query.json`
4. The application must parse the JSON and evaluate it against the rules specified in the audio.
5. If the JSON violates ANY of the rules, print exactly `REJECT` to standard output. If it passes all rules, print exactly `ACCEPT`.

The JSON format for the queries looks like this:
```json
{
  "source_document": "user_profiles",
  "graph_mapping": {
    "node_label": "User",
    "joins": [
      {
        "type": "inner",
        "target": "user_transactions",
        "condition": "user_profiles.id = user_transactions.user_id"
      }
    ]
  },
  "pagination": {
    "limit": 50,
    "offset": 0
  }
}
```

Ensure your Rust program correctly handles cases where fields might be missing or malformed according to standard deserialization logic (malformed JSON should also be REJECTed).

We will test your compiled binary against two hidden directories of JSON files: a "clean" corpus and an "evil" corpus. To succeed, your tool must correctly ACCEPT 100% of the clean corpus and REJECT 100% of the evil corpus.