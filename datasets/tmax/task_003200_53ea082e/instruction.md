You are acting as a backup administrator managing an automated archival system. We've discovered that our log rotation scripts frequently race with the writing processes, resulting in corrupted or maliciously structured tar archives. To secure our extraction pipeline, we need you to develop an intelligent Go-based archive sanitizer and resolve an incident.

First, an incident report was left by the previous admin as an audio recording. Please transcribe the audio file located at `/app/audio/incident_report.wav`. Write the exact text of the spoken transcription into `/home/user/transcript.txt`. You may use whisper, ffmpeg, or any available tools to recover the speech. 

Second, based on the need to prevent "tar slip" and malicious symlink attacks during log backup extractions, you must write a Go program located at `/home/user/tar_sanitizer.go`. 

Your Go program must behave as follows:
1. It will be invoked from the command line: `go run /home/user/tar_sanitizer.go <path_to_tar_file>`
2. It must read the `.tar` file specified (you do not need to handle gzip/bz2, just uncompressed tar).
3. It must analyze the archive's headers to detect malicious paths, symlinks, or hardlinks. 
4. It must REJECT the archive if any of the following are found:
   - Any file name or path that is absolute (starts with `/`).
   - Any file name or path that uses `../` to resolve outside the base root directory of the archive.
   - Any symbolic link (symlink) or hard link whose target is absolute (starts with `/`).
   - Any symbolic link whose target uses `../` to resolve outside the base root directory of the archive.
5. If the archive is safe, the program must print `ACCEPT` to standard output and exit with status code `0`.
6. If the archive violates any of the safety rules, it must print `REJECT` to standard output and exit with status code `1`.

Your solution will be tested against a massive corpus of both clean log backups and intentionally crafted "evil" archives containing malicious link and path traversals. Ensure your Go code correctly resolves path normalizations.