You are a data engineer responsible for processing automated voice notes into our analytics pipeline. Your goal is to build an ETL script that transcribes audio, normalizes the text, performs statistical stratification, and runs on a schedule.

An audio file containing a voice note has been dropped at `/app/audio_logs/dictation.wav`.

Please perform the following steps:

1. **Transcription & Normalization**:
   Write a Python script at `/home/user/etl_pipeline.py` that transcribes the audio file (you may install and use libraries like `openai-whisper`). 
   Once transcribed, tokenize the text into words and normalize it:
   - Convert all characters to lowercase.
   - Remove all punctuation (keep only alphanumeric characters `a-z0-9` and spaces).
   - Ensure the text is separated by single spaces.
   Save this normalized string to `/home/user/full_transcript.txt`.

2. **Stratified Sampling**:
   In the same Python script, analyze the word lengths in your normalized transcript. 
   Generate a stratified sample of exactly 30 words from the transcript. The distribution of word lengths in your sample must proportionally match the distribution of word lengths in the full transcript as closely as possible (use standard rounding to integer counts; if rounding causes the sum to deviate from 30, adjust the counts of the most frequent word lengths to ensure exactly 30 words are sampled).
   Save this sample as a JSON array of strings to `/home/user/stratified_sample.json`.

3. **Pipeline Scheduling**:
   We need this pipeline to run automatically. Configure a user-level cron job that executes your `/home/user/etl_pipeline.py` script every day exactly at 04:30 AM.

Your pipeline's accuracy will be evaluated programmatically. The primary metric is the Transcription Accuracy (calculated as 1.0 - Word Error Rate) of your `/home/user/full_transcript.txt` compared to a high-quality human baseline.