You are a localization engineer managing a pipeline that translates and transcribes spoken audio into English. Recently, we have noticed that some submitted audio translations are completely misaligned, contain anomalous noise/silence patterns, or fail basic constraint validations (e.g., length mismatch, nonsensical character repetitions). 

We have two corpora of transcription data generated from audio snippets:
- `/app/corpus/clean/`: Contains JSON files representing valid, well-formed English transcriptions (e.g., `{"id": 1, "text": "This is a valid translation.", "duration": 3.5}`).
- `/app/corpus/evil/`: Contains JSON files with anomalous transcriptions (e.g., random character strings, repeated words denoting a stuck pipeline, extreme length mismatches relative to duration, or gibberish).

Additionally, there is a reference audio file at `/app/audio/sample_issue.wav` which you must transcribe using a simple tool (like `whisper` if installed, or assume a given mock transcription output for testing) to understand the type of anomalies we are seeing (it contains a repeated anomalous phrase).

Your task is to write a Python script at `/home/user/detector.py` that acts as a filter.
1. It must take a directory path containing JSON transcription files as an argument.
2. It should analyze the text and duration using mathematical anomaly detection techniques (e.g., character frequency constraints, text length to duration ratio validation, Levenshtein distance against known gibberish patterns, or detection of repeating changepoints).
3. It must print the names of the files it classifies as "clean" to stdout, one per line. Files classified as "evil" (anomalous) should not be printed.
4. It must log its processing steps and decisions to `/home/user/pipeline.log`.

The script must correctly accept 100% of the clean corpus and reject 100% of the evil corpus.

Ensure your Python script is executable and can be run as:
`python3 /home/user/detector.py <directory_path>`