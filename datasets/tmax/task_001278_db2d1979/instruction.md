You are assisting a wildlife acoustics researcher in organizing a large, crowdsourced dataset of bird recordings. The incoming data contains metadata files that are sometimes malformed or contain malicious shell injections in the text fields (since the data is scraped from an untrusted web portal). 

Your task is to build a robust Bash-based data processing pipeline that verifies the integrity of the incoming archive, extracts a signature from a reference audio file, and securely filters the metadata files.

**Step 1: Extract the Reference Signature**
We have a reference calibration recording at `/app/reference_recording.wav`. 
1. Transcribe the spoken phrase in this audio file (you may install and use any tools necessary, such as `whisper` or `ffmpeg`, or APIs if accessible, but local transcription is preferred).
2. Format the transcribed text by converting it entirely to UPPERCASE and removing all punctuation. This string will be your `DATASET_SIGNATURE`.

**Step 2: Archive Verification and Decompression**
There is a compressed dataset archive at `/app/incoming_data.tar.gz`.
1. Verify its integrity and extract it to `/app/staging/`.
2. Inside, you will find hundreds of `.txt` metadata files.

**Step 3: Build the Sanitization Filter**
Write a Bash script at `/home/user/filter.sh` that takes exactly two arguments: an input directory and an output directory (`/home/user/filter.sh <input_dir> <output_dir>`).
This script must process every `.txt` file in the input directory and apply the following rules:

*   **Rule 1 (Configuration):** Read `/app/dataset.conf`. It contains a comma-separated list of required metadata keys (e.g., `Date,Location,Species`). The input `.txt` file (which consists of `Key: Value` lines) MUST contain all the required keys. If any are missing, reject the file.
*   **Rule 2 (Sanitization):** The file MUST NOT contain any of the following shell metacharacters anywhere in its contents: `;`, `|`, `&`, `$`, or `` ` `` (backtick). If it does, reject the file as potentially malicious.
*   **Rule 3 (Transformation):** If the file passes Rule 1 and Rule 2, copy it to the `<output_dir>`. You must append a new line to the end of the copied file exactly matching: `Signature: <DATASET_SIGNATURE>` (replace `<DATASET_SIGNATURE>` with the string obtained in Step 1).

**Step 4: Integration**
Run your script to process the extracted dataset:
`/home/user/filter.sh /app/staging /home/user/final_dataset`

*Note: An automated verification suite will test your `/home/user/filter.sh` against a hidden corpus of "clean" and "evil" metadata files to ensure your logic is perfectly sound.*