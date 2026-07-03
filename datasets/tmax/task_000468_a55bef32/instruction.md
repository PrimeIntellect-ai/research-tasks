You are helping a linguistics researcher automate their dataset ingestion pipeline for field recordings. 

You need to create a Python daemon that watches a directory for new archive files, extracts and standardizes the audio, transcribes it, and serves the results over an HTTP API.

Here are your instructions:

1. Create a directory `/home/user/incoming_archives` and another called `/home/user/processed_audio`.
2. Write and run a Python service that does the following:
   - Continuously watches `/home/user/incoming_archives` for new `.zip` files.
   - When a `.zip` file is detected, extracts its contents.
   - Finds any audio files within the extracted contents and converts them to 16kHz, mono `.wav` format.
   - Bulk renames the standardized audio files to the format `field_record_<md5_hash_of_standardized_file>.wav` and saves them in `/home/user/processed_audio`.
   - Transcribes the standardized audio files using `openai-whisper` (you should install it and use the `tiny.en` model).
   - Starts an HTTP server listening on `0.0.0.0:8000`.
   - Exposes an endpoint `GET /api/dataset` that returns a JSON object mapping the newly generated filenames (e.g., `field_record_...wav`) to their recognized transcription text.

3. We have received a new raw recording from the field, located at `/app/field_note.wav`. To test your pipeline, package this file into a zip archive named `test_batch.zip` and place it into `/home/user/incoming_archives`.

4. Wait for your daemon to process the file and update the API. Keep the daemon running in the background or in a separate terminal session so the verifier can test the API.

Make sure you install any necessary system or Python dependencies (e.g., `ffmpeg`, `watchdog`, `flask`, `openai-whisper`).