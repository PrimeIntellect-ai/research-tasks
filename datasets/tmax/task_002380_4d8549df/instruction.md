You are an AI assistant acting as an artifact manager for a binary repository. We have received an ingestion bundle containing a large raw audio recording and a multi-line ingestion log. The log indicates which parts of the audio are valid artifacts and which parts are noise or corrupt data.

Your task is to parse the log, extract the valid audio segments, merge them, transcribe the merged audio, and generate a cryptographic manifest of the individual chunks. 

Here are the specific requirements:

1. **Input Files**:
   - Audio File: `/app/audio/source.wav`
   - Log File: `/app/metadata/ingest.log`

2. **Log File Parsing**:
   The log file contains multi-line records separated by `---`. Each record looks like this:
   ```
   Record ID: <alphanumeric>
   Status: <Valid | Corrupt | Review>
   Start Time: <float seconds>
   End Time: <float seconds>
   ```
   You must parse this file to identify all records with the Status `Valid`.

3. **Audio Chunking and Merging**:
   - Write a Python script to split `/app/audio/source.wav` into individual segments based on the `Start Time` and `End Time` of each `Valid` record.
   - Save these individual valid chunks as WAV files in the directory `/home/user/chunks/` with the naming convention `chunk_<Record ID>.wav`.
   - Merge all the `Valid` audio segments in the exact order they appear in the log into a single contiguous audio file at `/home/user/curated.wav`.

4. **Manifest Generation**:
   - Generate a JSON manifest file at `/home/user/manifest.json`.
   - The manifest should be a dictionary where the keys are the chunk filenames (e.g., `chunk_A1.wav`) and the values are their SHA256 checksums (hex digests).

5. **Transcription**:
   - Install an open-source transcription library of your choice (e.g., `openai-whisper` or `SpeechRecognition`) in your Python environment.
   - Transcribe the spoken content of the merged audio file (`/home/user/curated.wav`).
   - Save the raw text transcription to `/home/user/transcript.txt`. Format it as a single line of text with no line breaks.

Your final evaluation will be based on the accuracy of your transcript compared to the hidden ground truth (evaluated using Word Error Rate), the correctness of the generated SHA256 manifest, and the successful extraction of the audio chunks.