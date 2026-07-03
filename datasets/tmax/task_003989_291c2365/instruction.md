You are an AI assistant helping a medical researcher organize and serve a messy dataset. 

I have a directory of raw research data located at `/app/research_data/`. It contains a mix of structured metadata files and raw audio recordings of patient interviews.

Your task is to parse the metadata, transcribe the audio, calculate checksums, and expose the organized data via a secure local web service.

Here are the specific requirements:

1. **Environment Setup & Transcription:**
   - There is a raw audio file at `/app/research_data/interview_sample.wav`.
   - You must generate a text transcript of the spoken content in this audio file. You may install and use any offline Python transcription tools you prefer (e.g., `openai-whisper`, `SpeechRecognition`, or `pocketsphinx`).

2. **Data Parsing & Manifest Generation:**
   - The directory also contains two metadata files: `/app/research_data/index.csv` and `/app/research_data/metadata.xml`.
   - Cross-reference these files to find the `participant_id` (from the CSV) and the `location` (from the XML) associated with `interview_sample.wav`.
   - Copy the audio file to a new directory: `/home/user/organized_data/interview_sample.wav`.
   - Calculate the SHA256 checksum of the audio file.
   - Generate a consolidated manifest file at `/home/user/organized_data/manifest.json`. It must be a JSON array of objects. The object for this audio file must contain exactly these keys:
     - `"filename"`: "interview_sample.wav"
     - `"checksum"`: the SHA256 hash string
     - `"participant_id"`: extracted from the CSV
     - `"location"`: extracted from the XML
     - `"transcript"`: the transcribed text (all lowercase, no punctuation)

3. **Data Serving (API Integration):**
   - Write and start a Python HTTP service running in the background.
   - The service must listen on `127.0.0.1` port `9090`.
   - It must expose an endpoint: `GET /api/v1/record?file=interview_sample.wav`
   - The endpoint must return the exact JSON object from your manifest for the requested file (with `Content-Type: application/json`).
   - **Security:** The endpoint must enforce authentication. It should only return the data if the request includes the HTTP header: `Authorization: Bearer delta-v-2024`. If the header is missing or incorrect, return a `401 Unauthorized` status.

Leave the web service running in the background when you are finished.