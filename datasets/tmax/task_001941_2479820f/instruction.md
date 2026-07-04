You are a data engineer tasked with building an extraction script for a new ETL pipeline. We have a legacy SQLite database at `/app/network.db` that stores a graph of internal corporate network connections. 

Recently, the database suffered a corruption issue. The main `relationships` table has a corrupted index, meaning queries against it frequently return stale or "ghost" rows that no longer exist in reality. 

The previous engineer who investigated this left a voicemail before departing. You can find the audio file at `/app/voicemail.wav`. You will need to transcribe or listen to this audio file (you may install tools like `openai-whisper` or `SpeechRecognition` + `pocketsphinx` via pip, or use `ffmpeg` to process it) to understand the correct reverse-engineered schema logic to bypass the corruption and extract valid graph edges.

Your objective:
Write a Python script at `/home/user/etl_extractor.py`.
The script must take exactly one command-line argument: a `node_id` (string).
Based on the instructions in the voicemail, the script must query `/app/network.db` for all VALID outgoing connections from that `node_id`.
The script must print a single JSON array to standard output containing the target `node_id`s (as strings) of all valid outgoing connections, sorted alphabetically. Do not print any other text.

Example usage:
`python3 /home/user/etl_extractor.py "NODE_050"`
Expected output format:
`["NODE_089", "NODE_102", "NODE_200"]`

Make sure your script handles missing nodes by outputting an empty JSON array `[]`.