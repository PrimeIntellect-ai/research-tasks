You are assisting a field researcher who is organizing a massive acoustic and telemetry dataset. 

The researcher recently recorded a voice memo dictating the exact rules for parsing the telemetry logs and generating the new bulk-renaming manifest. Unfortunately, they didn't write these rules down. The voice memo is located at `/app/voice_memo.wav`.

Your task has two parts:

1. **Transcription & Rule Extraction:** 
   Listen to or transcribe the audio file at `/app/voice_memo.wav` to recover the hidden data transformation rules. You may use any available Python libraries (e.g., `SpeechRecognition`, `pocketsphinx`), local tools, or API calls to transcribe the audio. The audio dictates specific logical conditions for how JSON log records map to new file names.

2. **Implement the Transformation Script:**
   Write a Bash script at `/home/user/rename_mapper.sh`. 
   - The script must read a stream of multi-line JSON records from `STDIN`. Each record contains metadata about a file (e.g., `file_id`, `timestamp`, `status`, `confidence`). 
   - The script must use stream processing tools (like `jq`, `awk`, `sed`) to parse this structured format.
   - For every valid record, it must print exactly one line to `STDOUT` representing the rename operation, formatted exactly as the voice memo dictates.
   - The script must be executable (`chmod +x`).

To ensure your script is completely robust, the system will test `/home/user/rename_mapper.sh` against a rigorous fuzzing verifier. It will generate hundreds of random JSON log streams and pipe them into your script. Your script's standard output must identically match the researcher's reference implementation (bit-exact equivalent) on all fuzzed inputs. 

Ensure your script handles edge cases implicitly covered by the dictated rules, cleanly skipping invalid streams or records as instructed.