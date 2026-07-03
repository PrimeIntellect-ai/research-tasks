You are an IT Storage Administrator tasked with auditing a set of legacy backup archives to reclaim disk space, while adhering to an emergency protocol left by the previous admin on a voicemail.

Your workflow involves parsing an inventory, verifying archive integrity, extracting and converting metadata, and writing a network service in C to report your findings to the automated auditing system.

Step 1: The Voicemail (Audio)
You will find an audio file at `/app/voicemail.wav`. The previous administrator recorded an emergency authorization code in this voicemail. You must transcribe this audio to recover the single-word code (it will be a phonetic alphabet word like "alpha", "bravo", etc.). 

Step 2: Archive Auditing
In `/app/storage/`, there are several archives (`.zip` and `.tar.gz`) listed in `/app/inventory.csv`. 
Some of these archives are corrupted. You must:
1. Verify the integrity of every archive.
2. For the archives that are INTACT (valid), extract the `manifest.xml` file contained within them.
3. The extracted `manifest.xml` files are encoded in `UTF-16LE`. Convert them to `UTF-8` and parse them to find the numeric value inside the `<bytes>` tag. Sum these values to get the `total_valid_bytes`.

Step 3: The Reporting Server (C)
Write a C program that acts as a TCP server listening on `127.0.0.1:8888`. This server must handle incoming TCP connections and respond to the following newline-terminated commands:
- Command: `AUTH\n`
  Response: The exact authorization code word transcribed from the audio (in uppercase, followed by `\n`).
- Command: `CORRUPTED\n`
  Response: A comma-separated list of the filenames of the corrupted archives, sorted alphabetically (e.g., `backup2.zip,backup5.tar.gz\n`).
- Command: `TOTAL_BYTES\n`
  Response: The sum of the `<bytes>` extracted from the valid manifests (e.g., `1540300\n`).

Compile and run your C server in the background. It must remain running and able to handle multiple sequential requests from the auditing system.