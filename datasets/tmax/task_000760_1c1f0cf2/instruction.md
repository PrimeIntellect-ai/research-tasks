I need your help recovering and organizing a legacy project archive. The previous developer left a voice dictation with instructions, but then hastily split and custom-compressed the project files before departing. 

Here is what you need to do:
1. First, locate the audio dictation file at `/app/project_dictation.wav`. You will need to transcribe this audio file (you can use `whisper` or any similar audio transcription tool available in your environment) to find the passphrase and the specific instructions on how to structure the project directories.
2. In `/home/user/project_parts/`, you will find several file chunks named `archive.dat.part1`, `archive.dat.part2`, etc. These form a single multi-part archive. 
3. The developer used a custom compression scheme: after concatenating the parts, the binary data has been bitwise XOR'd with the passphrase spoken in the audio file. Once XOR-decrypted, the file is a standard gzip-compressed tarball (`.tar.gz`).
4. Write a script (in Python or your preferred language) to concatenate the parts, apply the XOR decryption using the spoken passphrase, and extract the resulting tarball into `/home/user/extracted_project/`.
5. Organize the extracted files into a new directory `/home/user/organized_project/` exactly according to the rules spoken in the audio dictation.
6. Finally, start an HTTP server listening on `127.0.0.1:8080` that serves the `/home/user/organized_project/` directory. The server must remain running in the foreground or background so I can fetch the files over HTTP.

Please complete the extraction, reorganization, and ensure the HTTP server is running and serving the correct files.