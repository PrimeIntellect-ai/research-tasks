I am a researcher organizing a vast dataset of field interviews, and I need your help to optimize my data pipeline, process some pending audio, and expose the results for my analysis dashboard. 

Here is the situation:
1. I have a SQLite database located at `/home/user/research_data.db`. It contains three tables: `interviews` (id, date, location, duration_seconds, status), `tags` (id, tag_name), and `interview_tags` (interview_id, tag_id). 
2. Running aggregations on this database is currently extremely slow. I need you to analyze the query plans and create the necessary indexes so that querying interviews joined with their tags, grouped by location and tag_name, runs efficiently.
3. Once optimized, write a Bash script at `/home/user/export_summary.sh` that queries the database to find the total duration of interviews per `tag_name` for the location 'Amazonas', and exports the result as a JSON file at `/home/user/amazonas_summary.json`. The JSON should be an array of objects, e.g., `[{"tag": "biodiversity", "total_duration": 4500}, ...]`.
4. The database shows that one specific interview (ID: 42, status: 'pending_transcription') is missing its transcript. The corresponding audio file is located at `/app/pending_interview.wav`.
5. I have placed a compiled `whisper-cli` binary and a tiny English model at `/app/whisper-cli` and `/app/ggml-tiny.en.bin` respectively. Use a bash pipeline to transcribe this audio file. Extract the raw text and save it to `/home/user/transcript.txt`.
6. Finally, my dashboard needs to pull this data automatically. Bring up a simple HTTP service running entirely via Bash (you can use `socat`, `nc`, or a bash script, but do not use Python/Node.js for the server itself) listening on `0.0.0.0:8080`.
   - When it receives an HTTP `GET /summary`, it should return the contents of `/home/user/amazonas_summary.json` with a `200 OK` status and `Content-Type: application/json`.
   - When it receives an HTTP `GET /transcript`, it should return the contents of `/home/user/transcript.txt` with a `200 OK` status and `Content-Type: text/plain`.

Please ensure the server stays running in the background or foreground so my dashboard can connect to it.