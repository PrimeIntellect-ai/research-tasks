You are an edge computing engineer building an automated voice-log ingestion pipeline for IoT devices. Devices on the local network will push their audio logs and metadata to a central Git repository on this node. Your goal is to configure the Git server, write the processing scripts, and test the pipeline.

Perform the following tasks:

1. **Repository Setup:**
   - Initialize a bare Git repository at `/home/user/iot_ingest.git`.

2. **Python Transcription Script:**
   - Write a Python script at `/home/user/process_audio.py`.
   - The script should accept a path to a WAV file as a command-line argument.
   - It must use the `openai-whisper` package (use the `tiny` model to ensure it runs quickly) to transcribe the audio.
   - The script should print only the recognized text to standard output. (You may need to install `openai-whisper` and any required system dependencies like `ffmpeg`).

3. **Git Hook Configuration:**
   - Create a `post-receive` hook in the bare repository.
   - When a push is received, the hook must:
     a) Extract the newly pushed tree into a working directory at `/home/user/latest_push/`.
     b) Read a file named `metadata.txt` from the push. Use standard text processing tools (`grep`, `awk`, or `sed`) to extract the value of the `owner:` field. (Assume lines like `owner: edge_device_alpha`).
     c) Execute your `/home/user/process_audio.py` script on the pushed `audio.wav` file.
     d) Append a single line to `/home/user/ingest.log` strictly in the following format:
        `Owner: <extracted_owner_name> | Transcript: <transcription_text>`

4. **Integration Testing:**
   - To verify your pipeline, clone the bare repository to `/home/user/test_clone`.
   - Copy the provided test audio artifact `/app/device_audio.wav` into the clone as `audio.wav`.
   - Create a `metadata.txt` in the clone with the following contents:
     ```
     device_id: 104
     owner: edge_device_alpha
     priority: high
     ```
   - Commit these two files and push to the bare repository (`origin master`).

The automated verifier will read `/home/user/ingest.log`, extract your transcript, and calculate its similarity to the hidden ground truth text using a string matching metric. You must achieve a similarity score of >= 0.80.