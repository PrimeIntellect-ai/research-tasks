You are an observability engineer tasked with fixing a broken log ingestion pipeline. The dashboard is failing because the log format from our legacy system changed, and the original parser was lost.

A senior engineer left a voice memo before going on leave.
1. Transcribe the audio file located at `/app/voicemail.wav`. (A transcription utility `whisper` is available in your environment, or you may use any Python library you prefer to process the audio).
2. The voicemail contains critical instructions regarding the expected timezone, locale configurations, and the exact string manipulation rules required for the new log parser.
3. Apply any system or environment configurations mentioned in the voicemail.
4. Write a Python script at `/home/user/parser.py`.
   - The script must read a single line of text from standard input (`stdin`).
   - It must parse the text according to the rules detailed in the voicemail.
   - It must print a single JSON object to standard output (`stdout`).
   - It must implement robust error handling for malformed lines as specified in the voicemail.

Your Python script will be rigorously tested against thousands of synthetic log lines to ensure it is bit-for-bit equivalent to our internal oracle parser. Do not add any extraneous output or debugging text to standard output.