You are a localization engineer managing a translation data pipeline. Recently, an ETL job that syncs our translation database crashed and retried multiple times, resulting in a large CSV dump with duplicate, conflicting records. Additionally, the project manager left a critical last-minute translation override in an audio file because they were away from their desk.

Your objective is to clean the dataset, build an orchestrating server in Go to serve the translations, and apply the update from the audio file.

**Step 1: Data Cleaning and Validation**
You have an ETL dump at `/app/translations_dump.csv` with the following columns: `timestamp,locale,key,translation`.
Because of the ETL retry bug, there are duplicate `(locale, key)` pairs. 
- You must deduplicate the records by keeping only the row with the most recent (highest) `(locale, key)` pair based on `timestamp` (integer epoch).
- Perform constraint-based data validation: drop any rows where `locale` is not exactly two lowercase letters (e.g., keep `en`, `es`, `fr`, drop `EN`, `eng`, `e1`).

**Step 2: Build the Orchestration Server in Go**
Write a Go server (save it to `/home/user/localeserver/main.go`) that loads your cleaned data into memory upon startup.
The server must support two protocols simultaneously:
1. **HTTP Protocol (Port 8080):** 
   - Listen on `0.0.0.0:8080`.
   - Endpoint: `GET /translate?locale={locale}&key={key}`
   - Response: JSON format `{"translation": "value"}`. Return 404 if the key/locale pair is not found.
2. **TCP Protocol (Port 9000):**
   - Listen on `0.0.0.0:9000`.
   - Accept streaming newline-delimited text updates.
   - Format: `<locale>:<key>:<translation>\n`
   - When a valid update is received via TCP, it must immediately update the translation in memory so subsequent HTTP requests reflect the change. (Invalid locales can be ignored).

**Step 3: Process the Audio Override**
There is an audio file located at `/app/override.wav` containing a dictated localization update. 
- Transcribe the audio file. You may install and use any tools you prefer (e.g., Python's `SpeechRecognition`, `ffmpeg`, etc.). The spoken content will dictate a locale, a key, and a new translation.
- Start your Go server in the background.
- Apply the transcribed override to your running server via the TCP protocol (Port 9000).

Leave the Go server running in the background when you finish your turn so that the automated verifier can test both the HTTP and TCP endpoints.