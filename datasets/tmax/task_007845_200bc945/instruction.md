You are a mobile build engineer responsible for maintaining an automated build pipeline for a native C library used in an Android application. The pipeline has recently broken after an environment update, and you need to restore it and implement some new post-build tracking features.

Your workspace is located at `/home/user/mobile_pipeline/`.

You must complete the following objectives:

1. **Fix the C Build:**
   - The build configuration is located in `/home/user/mobile_pipeline/Makefile` and the source code is in `/home/user/mobile_pipeline/src/core.c`.
   - Running `make` currently fails. Identify and fix the errors in both the Makefile and the C source file. 
   - Upon successful compilation, it should produce a shared object file at `/home/user/mobile_pipeline/build/libcore.so`.

2. **Develop the Post-Build Python Script:**
   - Write a Python script at `/home/user/mobile_pipeline/pipeline.py` that automates the post-build steps.
   - **Structured Data Transformation & Checksum:** The script must read the legacy build metadata from `/home/user/mobile_pipeline/metadata.xml`. It should extract the `version` and `target`. It must then compute the SHA256 checksum of the generated `libcore.so` file.
   - The script should output a new JSON file at `/home/user/mobile_pipeline/manifest.json` with the exact following structure:
     ```json
     {
       "version": "<extracted_version>",
       "file": "<extracted_target>",
       "sha256": "<computed_checksum>"
     }
     ```
   
3. **Database Schema Migration & Record Insertion:**
   - The OTA (Over-The-Air) update tracker uses an SQLite database located at `/home/user/mobile_pipeline/ota.db`. 
   - The current schema for the `releases` table is `(id INTEGER PRIMARY KEY, version TEXT, target TEXT)`.
   - Your Python script (`pipeline.py`) must migrate this schema by adding two new columns to the `releases` table: `checksum` (TEXT) and `status` (TEXT, default 'pending').
   - Finally, the script must insert a new row into the `releases` table with the extracted version, target, computed checksum, and the default 'pending' status.

Run your script to complete the pipeline. To allow for automated verification, ensure `make` works cleanly, `manifest.json` exists with the correct values, and `ota.db` has the updated schema and new row.