You are tasked with fixing a messy dataset produced by a failing ETL job. The job was designed to aggregate user telemetry, but network retries caused it to ingest thousands of duplicate records. To make matters worse, different retry attempts introduced slight formatting anomalies, meaning standard deduplication won't work without prior normalization.

The exact business logic for cleaning and normalizing these records was left in an audio message by the lead data engineer before they went on leave. 

Here is what you need to do:
1. Locate the audio message at `/app/voicemail.wav`. Transcribe or listen to it (you will likely need to download and install a transcription tool like whisper or use Python speech-to-text libraries) to understand the exact text normalization, deduplication, and sorting rules required.
2. Build an executable program at `/home/user/cleaner` that implements these rules.
3. Your program must read a stream of uncleaned text records from `stdin`, apply the exact normalization steps dictated in the voicemail, deduplicate the records, and output the final cleaned dataset to `stdout` following the exact sorting rules specified.
4. To ensure your implementation perfectly aligns with the required logic, we have provided an obfuscated reference binary (an "oracle") at `/app/oracle_filter`. This binary exhibits the exact correct behavior. 

Your final executable `/home/user/cleaner` will be tested using a highly rigorous fuzzing verifier. The verifier will generate thousands of random inputs and pipe them through both your program and the reference `/app/oracle_filter`. Your program's standard output must be bit-for-bit identical to the oracle's standard output for every possible input stream.

You may write your script in any language (Python, Bash, Rust, Go, etc.), but ensure it is marked as executable (`chmod +x /home/user/cleaner`) and correctly uses a hashbang (e.g., `#!/usr/bin/env python3`) if it is a script.