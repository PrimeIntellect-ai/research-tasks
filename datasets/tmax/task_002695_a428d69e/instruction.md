You are acting as a backup administrator responsible for archiving critical system incident data. 

We have experienced a severe incident, and you need to process the incident data and archive the configuration files of the affected servers. However, some configuration logs have been tampered with or corrupted during the incident, containing malicious payloads (like path traversals or shell injections).

You have two primary objectives:

1. **Extract Incident Key from Audio:**
   You have been provided with an audio artifact from the server room voicemail system at `/app/incident_report.wav`. Use the locally installed offline transcription tool at `/usr/local/bin/whisper` to transcribe this audio. The transcription will contain a spoken phrase in the format "The archive key is [WORD]". Extract this [WORD] (in all lowercase).

2. **Develop a Go-based Log Sanitizer and Archiver:**
   We have two directories of server configurations:
   - `/app/corpus/clean/`: Contains known good configuration files.
   - `/app/corpus/evil/`: Contains malicious or corrupted configuration files that must not be archived.
   
   Write a Go program at `/home/user/archiver.go` that acts as a CLI tool. When compiled to `/home/user/archiver`, it must accept a directory path as an argument.
   
   The program must iterate through all `.conf` files in the given directory and apply the following checks:
   - Reject any file where the content contains the strings `../` or `/bin/sh` or `eval(`.
   - Reject any file where the file name contains hidden characters or spaces.
   - For accepted (clean) files, the program must apply a text transformation: replace all instances of `DEBUG_LEVEL=0` with `DEBUG_LEVEL=1`.
   
   Your compiled Go program must be executed against the clean and evil directories. 
   - It must print "REJECTED: [filename]" to stdout for evil files.
   - It must print "ACCEPTED: [filename]" to stdout for clean files.
   
3. **Final Archiving:**
   Using bash utilities (like `tar` and `awk`), create an archive of only the ACCEPTED files from the clean corpus. Name this archive `/home/user/final_backup_[KEY].tar.gz`, replacing `[KEY]` with the word you extracted from the audio transcription.