You are acting as a capacity planner for our infrastructure team. We have a legacy monitoring system that generates synthesized audio alerts for resource usage anomalies. We need to build a pipeline to ingest these audio alerts, filter out the false alarms (which are unfortunately common due to a bug in the legacy system), and process the real capacity warnings.

Your task is to set up a robust, automated pipeline using Rust and user-level system services.

Here are the requirements:

1. **Storage Setup**:
   - Create a 50MB raw image file at `/home/user/alert_volume.img`.
   - Format it as `ext4`.
   - Mount it at `/home/user/alert_data` using a user-mountable approach (e.g., via `udisksctl` or utilizing a pre-configured fstab entry if you had root, but since you don't, use `fuse2fs` to mount it). 
   - Inside `/home/user/alert_data`, create the following directory structure:
     - `incoming/`
     - `processing/`
     - `archive/`
   - Create a symlink at `/home/user/current_alerts` pointing to `/home/user/alert_data/incoming`.

2. **Audio Processing and Classification**:
   - We have provided a sample audio alert at `/app/alert_sample.wav`.
   - We also have a corpus of transcribed alerts located at `/app/corpora/`.
     - `/app/corpora/clean/` contains text files of genuine capacity alerts.
     - `/app/corpora/evil/` contains text files of false alarms and automated spam that the legacy system generates.
   - Write a Rust program at `/home/user/alert_classifier` (a Cargo project).
   - This program must build a binary named `alert-filter`.
   - The binary should take two arguments: an input text file and an output directory.
     - Example: `alert-filter /path/to/transcript.txt /home/user/alert_data/archive/`
   - The program must classify the content of the text file. If it is a genuine alert (matching the patterns in the clean corpus), it should copy the file to the output directory and exit with code 0. If it is a false alarm (matching the evil corpus), it should discard it and exit with code 1.
   - You must design the classification logic to successfully pass 100% of the clean corpus and reject 100% of the evil corpus.

3. **Service Management**:
   - Create a bash wrapper script at `/home/user/process_alerts.sh` that checks `/home/user/current_alerts` for `.txt` transcripts, runs the Rust `alert-filter` on them, and moves processed files to the `archive/` directory.
   - Create a systemd user service (`~/.config/systemd/user/alert-processor.service`) that runs this bash script.
   - Configure the service to be a `oneshot` service.
   - Create a systemd user timer (`~/.config/systemd/user/alert-processor.timer`) to trigger the service every 1 minute.
   - Enable and start the timer.

4. **Audio Transcription Extraction**:
   - To prove your pipeline handles the audio artifact, manually transcribe the hidden message in `/app/alert_sample.wav` (you may install and use tools like `whisper-cli` or `ffmpeg` to aid you, or simply listen/process it if you can).
   - Save the exact transcribed text into `/home/user/alert_data/incoming/sample_transcript.txt`.
   - Ensure the timer triggers your service, which should successfully process this transcript using your Rust classifier.

Log your final status by writing "PIPELINE ACTIVE" to `/home/user/status.log`.