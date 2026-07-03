You are a localization engineer managing a text translation pipeline. We recently received a new batch of translations in a CSV file, but our current Bash-based processing pipeline is silently dropping rows that contain embedded newlines within quoted fields, and we are serving outdated translations.

Your task is to build a robust localization pipeline using Bash and standard Linux CLI tools that accomplishes the following:

1. **Extract Version Tag**: 
   There is an image file located at `/app/version_tag.png` containing a watermark with the current release version. Use OCR (`tesseract`) to extract this text. Clean up any trailing whitespace from the extracted text.

2. **Process and Fix the CSV**:
   Read `/app/translations.csv`. The format is `Key,Lang,Source,Translation`. 
   - Some `Translation` fields are enclosed in double quotes and contain embedded newlines. You must correctly parse these without breaking or dropping them.
   - Perform Hash-based deduplication: Compute the MD5 hash of the `Source` string. If you encounter a `Source` string whose MD5 hash has already been processed in this run, skip the row.
   
3. **Template-based Text Generation**:
   For each valid, non-duplicate row, generate a localized text file at `/app/output/<Lang>/<Key>.txt`. The file must exactly match this template:
   ```
   Release: {Extracted_OCR_Version}
   Locale: {Lang}
   String ID: {Key}
   
   {Translation}
   ```
   *(Ensure the double quotes surrounding the translation in the CSV are removed in the final output, but preserve the embedded newlines).*

4. **Pipeline Logging**:
   For every file successfully generated, append a log line to `/app/pipeline.log` in the exact format:
   `[PROCESS] Created template for <Lang> - <Key> (Hash: <MD5_of_Source>)`

5. **Serve the Translations**:
   Write a bash script at `/app/serve.sh` that brings up an HTTP server listening exactly on `127.0.0.1:9090`. The server must serve the contents of the `/app/output/` directory. When an HTTP `GET /<Lang>/<Key>.txt` request is made, it should return the corresponding generated text file with a `200 OK` HTTP status. You may use standard CLI tools (e.g., `python3 -m http.server`, `nc`, or `socat`) within your bash script to achieve this, as long as it listens on the correct port and interface. Run this script in the background.

Ensure all directories are created with appropriate permissions.