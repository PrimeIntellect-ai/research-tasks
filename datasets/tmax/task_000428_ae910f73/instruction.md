You are a QA engineer tasked with setting up a robust test environment for a polyglot build orchestration system. We are migrating our internal build configuration schemas from version 1.x.x to version 2.0.0. 

As part of this transition, you need to accomplish three things: extract legacy test configurations embedded in a test recording, build a bulletproof schema migrator in Python, and validate your migrator against our test corpora to ensure no corrupted or malicious configurations crash the pipeline.

**Step 1: Extract Test Configurations from Video**
We have a test recording at `/app/build_dashboard_capture.mp4`. The original QA suite embedded the build configurations (as JSON) directly into the video's primary subtitle track.
1. Extract the subtitle track from the video.
2. Write a script to parse the extracted subtitles. Ignore timestamps and subtitle sequencing metadata; extract only the raw JSON text payloads.
3. Save each valid JSON payload to `/home/user/video_configs/`, naming them sequentially as `config_1.json`, `config_2.json`, etc.

**Step 2: Build the Schema Migrator**
Create a Python script at `/home/user/migrator.py` that takes an input directory of JSON configuration files, validates them, migrates them if necessary, and writes them to an output directory.

**CLI Signature:**
`python3 /home/user/migrator.py --input-dir <input_dir> --output-dir <output_dir> --reject-log <reject_file>`

**Migration & Validation Rules:**
1. **Deserialization & Validation:** Every file must be valid JSON. 
2. **Semantic Versioning:** The payload must have a `"version"` key following strict SemVer format (`MAJOR.MINOR.PATCH`, e.g., `1.2.0`). If the version is invalid (e.g., `1.2`, `v1.0.0`, `1.a.0`), the file must be REJECTED.
3. **Schema V1 (needs migration):** If version is `< 2.0.0`:
   - Must contain a `"build_steps"` key, which is a list of objects.
   - Each object must have `"lang"` (must be exactly `"cpp"`, `"python"`, or `"rust"`) and `"cmd"` (a string).
   - *Action:* Migrate this to V2 schema.
4. **Schema V2 (already up-to-date):** If version is `>= 2.0.0`:
   - Must contain an `"orchestration"` key, mapping languages (`"cpp"`, `"python"`, `"rust"`) to an object containing `"commands"` (a list of strings).
   - *Action:* Simply copy to output.
5. **Rejection:** Any file missing required keys, containing an unsupported language, having an invalid SemVer, or exhibiting schema mismatch must be REJECTED.
6. **V1 to V2 Translation:**
   - `"version"` becomes `"2.0.0"`.
   - V1 `{"build_steps": [{"lang": "python", "cmd": "pip install"}, {"lang": "python", "cmd": "pytest"}]}`
   - Becomes V2 `{"orchestration": {"python": {"commands": ["pip install", "pytest"]}}}`. Note how multiple steps for the same language consolidate their commands into a single list in the order they appeared.
7. **Output:** For accepted files, write the JSON to `<output_dir>/<filename>`. For rejected files, write the filename (e.g., `config_3.json`) on a new line to `<reject_file>`. DO NOT copy rejected files to the output directory.

**Step 3: Verification against Corpora**
We have provided an adversarial verification corpus:
- Valid configurations: `/app/corpora/clean/`
- Corrupt/Malicious configurations: `/app/corpora/evil/`

Your `migrator.py` must perfectly accept and migrate 100% of the clean corpus, and perfectly reject 100% of the evil corpus. Use these to test your script.

Finally, run your migrator on the extracted video configurations:
`python3 /home/user/migrator.py --input-dir /home/user/video_configs/ --output-dir /home/user/video_configs_migrated/ --reject-log /home/user/video_rejects.log`