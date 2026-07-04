You are tasked with building a specialized ETL pipeline for an acoustic monitoring system. We have a set of continuous audio recordings from a remote sensor network that capture both environmental events and spoken field notes.

Your goal is to process a provided audio recording, extract specific acoustic features, transcribe the speech, and output a structured dataset.

Specifically, you must:
1. Locate the audio recording at `/app/data/field_recording.wav`.
2. Write a Python script `/home/user/pipeline/process_audio.py` that reads the audio file and extracts the first 13 Mel-frequency cepstral coefficients (MFCCs) at a 10ms frame rate (with a 25ms window). Resample the audio to 16kHz before feature extraction if necessary.
3. Use a lightweight transcription tool or library (e.g., `SpeechRecognition` with Sphinx, or a small Whisper model if you install it) to transcribe the spoken segments in the audio file.
4. Integrate the text transcription and the summarized acoustic features (mean and variance of the 13 MFCCs across the entire file) into a single JSON file.
5. The output JSON must be saved at `/home/user/output/analysis.json` and must have the following structure:
```json
{
  "transcription": "...",
  "mfcc_mean": [val1, val2, ..., val13],
  "mfcc_var": [val1, val2, ..., val13]
}
```
6. Set up a cron job that schedules this script to run every 15 minutes, logging its output to `/home/user/output/pipeline.log`. Provide a setup script `/home/user/setup_cron.sh` that installs the cron job.

The success of your pipeline will be evaluated by comparing your extracted MFCC means to our reference implementation. Your results must fall within a strict Mean Squared Error (MSE) threshold.