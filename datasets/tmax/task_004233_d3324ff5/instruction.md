You are a backup administrator tasked with archiving critical incident audio logs for an automated data center. 

Your workflow requires identifying specific incident recordings, staging them securely using hard links, and extracting their spoken contents for full-text search indexing.

Your task is to write and execute a Bash-based workflow to accomplish the following:

1. **Configuration File Interpretation:**
   Read the configuration file at `/app/config/backup.ini`. It contains various settings, but you specifically need to extract the value of `TargetEventType` under the `[Archival]` section.

2. **Multi-line Log Record Parsing:**
   Parse the system log file at `/app/logs/system_events.log`. This log contains multi-line records. Find the record where the `Type:` matches the `TargetEventType` you found in the configuration. Extract the exact `Date:` and `Time:` (format: `YYYY-MM-DD HH:MM:SS`) from this specific multi-line record.

3. **Metadata-based File Search:**
   Search the directory `/app/recordings/` for a `.wav` file. You must find the file whose filesystem modification time exactly matches (within a 1-minute window) the date and time of the critical event you extracted from the log.

4. **Hard Link Management:**
   Create the directory `/app/archive/` if it does not exist. Create a hard link of the identified `.wav` file into `/app/archive/` using its original filename.

5. **Audio Transcription & Dependencies:**
   The archived audio must be transcribed so its contents can be indexed. 
   - You must install an open-source audio transcription tool of your choice (e.g., `whisper` via pip, `ffmpeg`, or compile `whisper.cpp`). You have internet access to install necessary dependencies.
   - Run the transcription tool on the hard-linked audio file.
   - Save the raw transcribed text into `/app/archive/transcript.txt`. The file should contain nothing but the spoken English text.

Your final deliverable is the successfully created `/app/archive/transcript.txt` file containing the accurate transcription of the correct audio file, along with the hard-linked `.wav` file in `/app/archive/`. Ensure your Bash scripts and commands are robust enough to handle the end-to-end process.