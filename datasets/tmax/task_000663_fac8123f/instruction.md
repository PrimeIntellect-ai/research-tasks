You are acting as a Database Administrator. We are dealing with a severe issue in our document-graph hybrid database where a corrupted index is causing queries to return stale and inconsistent hierarchical records. 

The Lead Engineer left an urgent voicemail explaining the exact condition that makes a record "stale". The voicemail is located at `/app/voicemail.wav`.

Your task:
1. Transcribe the audio file `/app/voicemail.wav` to understand the business logic for identifying stale records. You may use any tools available in the environment to process the audio.
2. Based on the rules described in the audio, create a filter tool that can inspect our database JSON export payloads and classify them. 
3. Write an executable script at `/home/user/check_payload.sh`. This script must take exactly one argument: the absolute path to a JSON file containing a hierarchical document.
4. Your script must traverse the hierarchical JSON structure and determine if the document is clean or stale.
   - If the document is CLEAN, the script must exit with status code `0`.
   - If the document is STALE (violates the conditions in the voicemail), the script must exit with status code `1`.

The JSON documents have a recursive structure where a node may contain an array of child nodes under the key `dependencies`. Each node has `node_id`, `last_modified` (an integer timestamp), `status` (a string), and `dependencies` (a list of child nodes).

Ensure your script works efficiently for deeply nested trees. Do not modify the JSON files; just exit with the appropriate status code.