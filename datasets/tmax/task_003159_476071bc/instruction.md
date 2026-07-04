You are an IT support technician responding to an escalated ticket (Ticket #8819). The data engineering team has reported that their concurrent image ingestion pipeline, `/home/user/pipeline/ingest.py`, intermittently crashes or drops records. The user attached a screenshot of the terminal when the system crashed, located at `/app/ticket_8819_screenshot.png`.

Your objectives are:
1. Extract the failing "Batch ID" from the provided screenshot.
2. The ingestion script (`/home/user/pipeline/ingest.py`) is meant to process image metadata and write to an SQLite database (`/home/user/pipeline/metadata.db`). It suffers from intermittent failures (race conditions on DB writes) and breaks entirely when encountering files with spaces or special shell characters. Fix `ingest.py` so that it safely and concurrently processes all files in a given directory without dropping records or throwing exceptions. Write the extracted Batch ID to a log file at `/home/user/batch_id_recovery.log`.
3. To prevent future outages, write a standalone Python script `/home/user/validate.py` that acts as a strict filename validator. 
   - It must accept a single filename as a command-line argument (e.g., `python3 /home/user/validate.py "my file.png"`).
   - It should print exactly `SAFE` to stdout and exit with code 0 if the filename contains only alphanumeric characters, hyphens, and underscores, and ends with a valid image extension (`.png`, `.jpg`, `.jpeg`).
   - It should print exactly `UNSAFE` to stdout and exit with code 1 if the filename contains spaces, shell metacharacters, directory traversal attempts, or invalid extensions.

Your final deliverable for part 3 will be rigorously tested against a hidden corpus of known safe and malicious (adversarial) filenames.