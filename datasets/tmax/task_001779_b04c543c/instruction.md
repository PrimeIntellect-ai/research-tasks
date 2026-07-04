You are tasked with recovering the configuration state of a legacy server. The previous administrator used an eccentric configuration manager that output its changelog as a screen recording of a terminal rather than a text file. 

You have been provided with this video artefact at `/app/config_record.mp4`. The video displays a sequence of multi-line log records detailing changes made to the server's primary configuration file, `server_config.ini`.

Your objectives are as follows:

1. **Extract and Parse the Changelog:** 
   Extract the text from the video frames. The text scrolls, so you will need to deduplicate overlapping text to reconstruct the continuous changelog. 
   Each log record in the video follows this multi-line format:
   ```
   START_RECORD [YYYY-MM-DD HH:MM:SS]
   ACTION: <APPEND | DELETE>
   <PAYLOAD (for APPEND) or LINE_NUMBER (for DELETE)>
   END_RECORD
   ```

2. **Reconstruct the Configuration:**
   Starting with an empty file, apply the extracted changelog actions in chronological order to reconstruct the final state of `server_config.ini`.
   - `APPEND`: Add the payload text as a new line at the end of the file.
   - `DELETE`: Remove the line at the specified 1-based line number (e.g., `DELETE 3` removes the 3rd line of the current file state).

3. **Atomic File I/O & Chunking:**
   - Write the final reconstructed configuration to `/home/user/server_config.ini`. You must use an atomic write pattern (write to a temporary file first, then atomically rename it to the target path) to simulate safe deployment.
   - Split the full reconstructed text changelog into smaller chunks, each containing exactly 5 complete records. Save these chunks in `/home/user/parsed_logs/` with the naming convention `chunk_0001.log`, `chunk_0002.log`, etc.

You may install any required packages (e.g., `tesseract-ocr`, `ffmpeg`, OpenCV, etc.) to perform the frame extraction and OCR. Your success will be measured by a string similarity metric between your reconstructed `server_config.ini` and the hidden ground-truth file. Aim for a similarity score of at least 90% to pass.