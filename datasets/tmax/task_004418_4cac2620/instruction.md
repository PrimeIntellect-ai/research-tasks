You are an automation specialist setting up an alerting pipeline. We receive critical system alerts as audio files from a legacy monitoring system. Your task is to process these audio alerts, extract and normalize the data, enrich it with our inventory data, and serve the result via a simple HTTP API.

You have been provided with:
1. An audio file containing the latest alert at `/app/alert.wav`.
2. A CSV file containing our server inventory at `/home/user/nodes.csv`.

Perform the following steps using Python:
1. **Transcribe the audio**: Process `/app/alert.wav` to text. You may install and use `openai-whisper` (the `tiny.en` model is recommended for speed). 
2. **Extract and Normalize**: The audio will always follow the pattern: "System alert. Error code [Letter] [Digit] [Digit]. Server node [Word] [Digit]." (e.g., "...Error code E seven two. Server node omega nine.").
   - Write a regex-based extraction routine to pull the error code and the server node name from the transcript.
   - Normalize the extracted data: Convert the spoken digit words (e.g., "seven", "two", "nine") into numeric digits (e.g., "7", "2", "9").
   - Format the error code with a hyphen (e.g., "E-72").
   - Format the node name with a space (e.g., "omega 9").
3. **Data Join**: Look up the normalized node name in `/home/user/nodes.csv` to find the corresponding `ip_address` and `owner`.
4. **Template Generation**: Construct a JSON payload that exactly matches this structure:
   ```json
   {
     "error_code": "<normalized_error_code>",
     "node_name": "<normalized_node_name>",
     "node_ip": "<joined_ip_address>",
     "owner": "<joined_owner>"
   }
   ```
5. **Serve the Data**: Write and run a Python HTTP server (e.g., using `Flask`, `FastAPI`, or `http.server`) that listens on `127.0.0.1:8080`. 
   - It must expose a `GET /alert` endpoint.
   - When requested, it must return the generated JSON payload with a `200 OK` status and `Content-Type: application/json`.

Leave the server running in the background or foreground so that it can be queried for verification.