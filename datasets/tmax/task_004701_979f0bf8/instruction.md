You are a data scientist preparing a new dataset from raw audio logs. We have an audio file located at `/app/dataset_recording.wav` containing spoken data records.

Your goal is to transcribe, clean, tokenize, and track the processing of this dataset. Follow these precise steps:

1. **Transcription**: Use an open-source transcription model (such as OpenAI's `whisper` via Python) to transcribe the audio file into text.
2. **Dataset Cleaning**: Process the transcribed text with the following strict rules:
   - Convert all text to lowercase.
   - Remove all punctuation characters entirely (leave spaces intact).
   - Remove all instances of the filler words "um", "uh", and "like" when they appear as standalone words (e.g., do not remove the "like" in "likely", but remove it if it is the word "like"). Consolidate multiple spaces into single spaces.
3. **Tokenization and Validation**: Tokenize the cleaned string using the HuggingFace `bert-base-uncased` tokenizer. Group the resulting tokens into non-overlapping chunks of exactly 15 tokens. Discard any remaining tokens at the end that do not form a complete 15-token chunk.
4. **Experiment Tracking**: Log your final validated results to a JSON file at `/home/user/experiment_log.json`. The JSON must be a single dictionary with the following keys:
   - `"raw_transcript"`: (string) Your initial raw transcription.
   - `"cleaned_text"`: (string) The text after applying all cleaning rules.
   - `"total_tokens"`: (integer) The total number of tokens before chunking.
   - `"chunk_count"`: (integer) The number of valid 15-token chunks generated.

The automated verification system will read `/home/user/experiment_log.json`, extract your `"cleaned_text"`, and calculate the Word Error Rate (WER) against our verified, human-annotated ground truth. You must achieve a WER of 0.15 or lower to pass. 

Note: You may install necessary Python packages (like `openai-whisper`, `transformers`, etc.) in your local user environment. Assume `ffmpeg` is available on the system.