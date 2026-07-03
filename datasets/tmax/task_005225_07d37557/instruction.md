You are an AI assistant acting as a technical writer's tool. You have been given a set of files to process, update, and back up for a legacy project. 

Your tasks are to:
1. Extract the documentation archive located at `/app/docs.tar.gz` into the `/home/user/docs` directory.
2. Read the multi-line log file at `/app/edit_history.log`. Each record is separated by `---` and contains a `Commit`, `Date` (in YYYY-MM-DD HH:MM:SS format), `File`, and `Notes`. You must parse this file to determine which file in the documentation was the *most recently modified* based on the `Date` field.
3. Transcribe the technical notes dictated in the audio file `/app/dictation.wav`. You will likely need to write a Python script and install an offline transcription library (e.g., `SpeechRecognition` with `pocketsphinx`, or `openai-whisper` if you prefer, though lightweight models are recommended for speed).
4. Append the transcribed text (as a single line) to the bottom of the most recently modified file identified in step 2.
5. Create an archive at `/home/user/incremental.tar.gz` that contains *only* the documentation files that you have modified (an incremental/differential backup). Do not include unmodified files in this archive.

Constraints:
- You must use Bash scripts/commands for the archive extraction, log parsing, and incremental backup creation. Python may be used for the audio transcription.
- Ensure the incremental archive preserves the relative paths (e.g., `auth.md` or `chapter1/auth.md` depending on the structure).

Verification:
An automated test will evaluate the text you appended to the correct document. It will extract your `incremental.tar.gz` and use a string similarity metric (Python's `difflib.SequenceMatcher`) to compare your appended line against the ground-truth transcript. You must achieve a similarity score of >= 0.75 to pass.