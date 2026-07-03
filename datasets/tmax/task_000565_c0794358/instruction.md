You are acting as a localization engineer for a global software company. We are updating our translation pipelines, but we have a problem. Our legacy translation validation tool is a proprietary, compiled binary that crashes or corrupts data when it encounters specific malformed Unicode sequences or incorrect character encodings. 

We need you to build a Python-based filter/sanitizer that sits in front of this legacy binary. Your tool must process translation files (in JSON format) and filter out entries that contain unsafe strings, preserving the good ones. 

Here are the specifics:
1. There is a stripped, legacy binary located at `/app/legacy_validator`. This binary accepts a UTF-8 string as a command-line argument and exits with code 0 if it can process it, or a non-zero code if it fails. It implements a proprietary string normalization and length-checking algorithm.
2. You need to write a Python script at `/home/user/filter_translations.py`. 
3. Your script must read a JSON file containing a list of objects: `[{"id": "...", "lang": "...", "text": "..."}]`.
4. For each entry, your script should determine if the `text` field is safe. A text is safe if it is valid UTF-8, does not contain any unassigned Unicode code points, and does not cause the `/app/legacy_validator` to return a non-zero exit code.
5. Your script must use Python's `multiprocessing` or `concurrent.futures` to process the entries in parallel, as the legacy binary is slow.
6. The script should take two arguments: the input JSON file path and the output JSON file path. It must write a new JSON file containing only the safe entries, in the exact same format.

We will test your script against a hidden test suite containing an "evil" corpus (files with strings designed to break the pipeline or invalid encodings) and a "clean" corpus (perfectly valid translations). Your script must successfully filter out the bad entries while keeping 100% of the clean entries intact.

Please write the script `/home/user/filter_translations.py` and ensure it is executable.