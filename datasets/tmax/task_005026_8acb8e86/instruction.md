You are acting as a Localization Engineer. You need to compile updated translation strings from multiple vendors and formats, map them to specific UI screens in a product walkthrough video, and serve the result via an HTTP API.

Here is the situation:
1. We have a baseline localization file at `/home/user/locales_old.json`.
2. Vendor A provided updates in a CSV format at `/home/user/updates.csv`.
3. Vendor B provided updates in an XML format at `/home/user/vendor_translations.xml`.
4. We have a product walkthrough video at `/app/ui_walkthrough.mp4`. The video shows a sequence of UI screens.
5. The sequence of UI screen keys shown in the video is listed in `/home/user/sequence.txt` (one key per line). Each screen corresponds to a distinct scene in the video.

Your task:
1. **Data Integration & Normalization**:
   Read the JSON, CSV, and XML files. Merge them so that the newer updates (from the CSV and XML) overwrite any existing translations for the same key and language.
   - The CSV file has columns: `key`, `lang`, `text`.
   - The XML file has the structure: `<translations><item key="..." lang="...">...</item></translations>`.
   - Ensure all text is trimmed of leading/trailing whitespace and normalized to UTF-8 NFC form.

2. **Video Analysis**:
   The video `/app/ui_walkthrough.mp4` contains exactly 4 scenes (hard cuts). Extract the timestamps of these scene changes. 
   - The first scene starts at `0.0` seconds.
   - Map the chronological sequence of scenes to the keys listed in `/home/user/sequence.txt`.

3. **Service Deployment**:
   Create and start an HTTP REST API server listening on `0.0.0.0:8080`.
   The server MUST require an Authorization header: `Authorization: Bearer loc_token_99` for all requests (return 401 Unauthorized otherwise).

   Implement the following endpoints:
   - `GET /locales?lang={lang}`: 
     Returns a JSON object of all merged translations for the specified language. 
     Format: `{"ui_welcome": "Welcome", ...}`
   - `GET /subtitle?lang={lang}&time={seconds}`:
     Determines which scene is active at the given `time` (in seconds), finds the corresponding UI key from the sequence, and returns a JSON object:
     `{"key": "the_ui_key", "text": "the_translated_text"}`
     If the requested language does not have a translation for that key, fall back to the "en" (English) translation.

Keep the server running in the background or foreground so we can verify it. Write your implementation in Python, Node.js, or any language you prefer, as long as it listens on port 8080 and handles the requests as specified.