You are acting as a storage administrator tasked with managing disk space and handling a custom archival tool left behind by a former employee. 

We have a directory `/app/logs_incoming/` where legacy systems continuously write uncompressed log files. To save space, a custom archiving method was developed, but the source code for the archival tool was lost. However, the former employee left a voice memo detailing the exact custom encoding algorithm used for these logs.

There is an audio file located at `/app/voice_memo.wav`. You need to listen to or transcribe this audio file to understand the custom compression algorithm. 

Once you have determined the algorithm from the audio:
1. Write a Bash script at `/home/user/custom_archive.sh` that implements this exact compression algorithm. The script must read standard input and output the encoded "compressed" data to standard output.
2. Write a counterpart Bash script at `/home/user/custom_extract.sh` that reads the encoded data from standard input and outputs the original decoded data to standard output.
3. Identify all log files in `/app/logs_incoming/` that are older than 7 days (based on their modification time metadata) and rename them to have a `.archive_pending` extension. 

Your implementations in `custom_archive.sh` and `custom_extract.sh` will be rigorously tested against a reference binary to ensure bit-exact equivalence for any arbitrary input. Make sure your Bash scripts handle binary data safely.