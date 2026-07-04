You are a storage administrator tasked with cleaning up a massive backlog of uploaded archives. Your manager left you an urgent voicemail explaining the new compliance rules for storing user uploads, but the system only saved it as an audio file.

1. First, recover the spoken instructions from the voicemail located at `/app/voicemail.wav` (you may install and use transcription tools like `whisper-cli`, `ffmpeg`, or Python-based transcription libraries). 
2. The voicemail will tell you the exact criteria for "compliant" and "non-compliant" archive files based on their uncompressed contents.
3. Write a Python script at `/home/user/cleanup.py` that enforces these rules. The script must:
   - Accept a single command-line argument: the path to a directory containing `.tar.gz` files.
   - Iterate over all `.tar.gz` files in that directory.
   - Inspect the metadata of the contents of each archive *without extracting the files to disk* (use compressed stream processing in Python).
   - If an archive violates the rules specified in the voicemail, **delete** the archive from the disk.
   - If an archive complies with all rules, **rename** the archive in place by prepending `approved_` to its filename (e.g., `data.tar.gz` becomes `approved_data.tar.gz`).

Your script must perfectly classify and process the files. We will test your script by running it against a hidden evaluation directory containing both compliant and non-compliant archives.