You are an AI assistant helping a dataset researcher organize and sanitize a collection of interview records.

We have a set of dataset archives submitted by various external field teams. Unfortunately, some of these archives are malicious and contain "Zip Slip" payloads (path traversal vulnerabilities designed to overwrite files outside the extraction target). 

Additionally, we have a reference audio recording from a key interview.

Your objectives:
1. **Audio Transcription**: 
   There is an audio file located at `/app/reference_interview.wav`. Use Python (e.g., the `openai-whisper` package) to transcribe this audio file. Save the exact transcribed text to `/home/user/audio_transcript.txt`.

2. **Secure Archive Extractor and Parser**:
   Write a Python script at `/home/user/dataset_processor.py`. The script must take an input directory containing ZIP archives and a target output directory:
   `python3 /home/user/dataset_processor.py <input_dir> <output_dir>`

   The script must perform the following:
   - Iterate through all `.zip` files in `<input_dir>`.
   - Before extracting, inspect the contents of each ZIP. If ANY file inside the ZIP contains a malicious path (e.g., uses `../` to navigate up directories, or uses absolute paths), the script MUST REJECT the entire archive. Do not extract any files from a malicious archive.
   - For rejected archives, append the base filename (e.g., `submission_4.zip`) on a new line to `/home/user/rejected_archives.log`.
   - For clean archives, extract the contents safely into `<output_dir>/<archive_basename>/`.
   - Each clean archive contains a multi-line log file (`events.log`). Parse this file and convert it into a JSON file named `events.json` in the same extracted folder. The JSON should be an array of objects, where each object corresponds to a multi-line log entry.

3. **Execution**:
   Once your script is ready, run it against the untrusted submissions located in `/app/corpora/incoming/` and output the safe, parsed results to `/home/user/extracted_datasets/`.
   `python3 /home/user/dataset_processor.py /app/corpora/incoming /home/user/extracted_datasets`

Ensure your solution cleanly separates the malicious files from the safe ones, leaving the system secure.