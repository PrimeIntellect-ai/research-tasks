You are an artifact manager for a secure binary repository. Your organization receives hundreds of artifact bundles from external contractors, and you need to build a robust bash script to filter out malicious or non-compliant submissions.

Recently, our intelligence team intercepted a short radio transmission from a rogue contractor. The audio file is located at `/app/intercepted_comms.wav`. You must transcribe this audio (you may install and use any CLI transcription tools, like whisper.cpp or ffmpeg, to process it). The audio contains the name of a **banned project code**. Any artifact associated with this project code must be rejected.

Each submitted artifact is a compressed `.tar.gz` file containing:
1. Various binary or text payload files.
2. A `manifest.sha256` file containing the SHA-256 checksums of all the payload files.
3. A `metadata.txt` file containing information about the project. Due to a legacy contractor system, **`metadata.txt` is always encoded in `Shift_JIS`**.

Your task is to write a validation script at `/home/user/filter_artifacts.sh`. The script must take exactly one argument: the absolute path to a `.tar.gz` artifact file.

The script must evaluate the artifact and exit with code `0` (Accept/Clean) ONLY IF all of the following conditions are met. If any condition fails, it must exit with code `1` (Reject/Evil):

1. **Path Integrity:** The archive must not contain any absolute paths, nor any paths attempting directory traversal (e.g., containing `../`), nor any symlinks pointing outside the extraction directory.
2. **Manifest Verification:** All files listed in `manifest.sha256` must exist, and their computed SHA-256 checksums must perfectly match the hashes provided in the manifest.
3. **Encoding & Content Sanitization:** The script must extract `metadata.txt`, convert its character encoding from `Shift_JIS` to `UTF-8`, and scan the resulting text. If the converted text contains the **banned project code** (which you will discover by transcribing the audio file), the artifact must be rejected. 

For testing, we have provided two corpora of artifacts:
* Valid, compliant archives are located in `/app/corpora/clean/`
* Malicious or non-compliant archives are located in `/app/corpora/evil/`

Ensure your script is robust, uses standard bash facilities securely (handling spaces in filenames, cleaning up temporary mount/extraction directories, etc.), and strictly enforces the exit code rules.