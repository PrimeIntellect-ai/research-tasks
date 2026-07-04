You are a Database Reliability Engineer (DBRE) tasked with recovering backup dependency schemas after a catastrophic metadata corruption event. 

During the incident, the on-call engineer left an urgent voice memo specifying the critical "root of trust" backup server that must be present in any valid recovery schema. 

Your tasks are:
1. **Transcribe the Voicemail**: Extract the critical target node ID spoken in the audio file located at `/app/oncall_voicemail.wav`. (You may use tools like `whisper` or write a quick script using an available API if you mock it, or use `ffmpeg` / `whisper.cpp` provided in the environment).
2. **Develop a Schema Validator**: Write a script at `/home/user/validate_schema.sh` that takes a single file path as an argument. The script must analyze the JSON graph in the file and determine if it is a valid backup schema.
3. **Validation Rules**:
   To be considered valid, a schema MUST:
   - Contain the critical target node ID (spoken in the voicemail) in its `"nodes"` array.
   - Form a perfectly valid Directed Acyclic Graph (DAG) based on its `"edges"`. There must be **absolutely no cycles** (circular dependencies) in the graph.

**Input JSON Format:**
```json
{
  "nodes": ["node_1", "node_2", "node_3"],
  "edges": [
    {"from": "node_1", "to": "node_2"},
    {"from": "node_2", "to": "node_3"}
  ]
}
```

**Output Requirements for `validate_schema.sh`:**
- If the schema is valid (contains the target node AND has no cycles), the script MUST exit with code `0`.
- If the schema is invalid (missing the target node OR contains one or more cycles), the script MUST exit with a non-zero code (e.g., `1`).
- The script should be executable (`chmod +x`). You may write the internal logic in any language you prefer (e.g., Python, Bash, Node), as long as the entry point is the bash script.

You have access to a sample of corrupted and recovered schemas in your environment to test your logic if needed. Your final script will be strictly evaluated against a hidden, adversarial corpus of schemas.