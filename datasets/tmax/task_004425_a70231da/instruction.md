You are tasked with building a Voice-Assisted Configuration Management Tracker. 

Sysadmins have been leaving audio memos of configuration changes. We need a system that ingests these changes, validates them, anonymizes the admin names, deduplicates redundant changes, and serves the final configuration state over a custom TCP protocol.

Step 1: Audio Transcription
You have been provided with an audio file at `/app/config_memo.wav`. 
Transcribe this audio file. The audio contains several sentences, each specifying a configuration change in the format: "Set [key] to [value]. Admin [name]." 
(You may install and use Python's `SpeechRecognition` library, `whisper`, or any other tool you prefer to transcribe it. You will need to parse the resulting text to extract the keys, values, and admin names).

Step 2: The Configuration Server (C Programming)
Write a C program at `/home/user/config_server.c` and compile it to `/home/user/config_server`. 
This server must:
1. Listen for incoming TCP connections on `127.0.0.1:9090`.
2. Accept line-by-line commands (ending with `\n`).

Supported Commands:
- `ADD key=[key] value=[value] admin=[name]`
  When this command is received, the server should process the config change:
  - **Constraint Validation**: Ensure that the `value` is a positive integer (greater than 0). If it is not, drop the record.
  - **Data Masking**: Replace the `[name]` with `***` for privacy.
  - **Deduplication**: If a configuration with the same `key` already exists, update its `value` and `admin` (overwriting the old record), effectively deduplicating by the config key.
  - Send the response: `ACK\n`
- `DUMP`
  When this command is received, the server should return all valid, currently stored configurations, one per line, in the exact format:
  `CONFIG: key=[key] value=[value] admin=***\n`
  After sending all configurations, send `END\n` and close the connection.

Step 3: Integration
Start your server in the background. Then, using bash or a script of your choice, read the extracted data from your transcription of `/app/config_memo.wav` and send each parsed configuration to the server using the `ADD` command via `nc` (netcat) or similar.

Leave the server running on port 9090 when you are finished.