You are a data engineer tasked with building an ETL pipeline and a spam filter for a customer support audio transcription system.

We have a growing problem with automated bot calls leaving spam voice messages. We have accumulated a corpus of transcribed bot messages (evil) and real customer messages (clean). We also have a new incoming audio file that needs to be processed.

Your tasks are:

1. **Audio Transcription & ETL**
   Write a Bash script `/home/user/process_audio.sh` that takes an audio file path as an argument.
   - It should transcribe the audio file located at `/app/audio/support_call.wav` (you may use `whisper` or any installed python whisper module to generate the transcript).
   - Extract the pure text of the transcription.
   - Join the text with the customer's metadata. The metadata is located at `/app/data/metadata.csv` (format: `filename,customer_id,account_tier`). The filename for this audio is `support_call.wav`.
   - The script should append a line to `/home/user/etl_output.log` in the format:
     `[customer_id] | [account_tier] | [TRANSCRIPT_TEXT]`

2. **Spam Filter Development (Adversarial Corpus)**
   Write a Bash script `/home/user/filter.sh` that acts as a spam classifier.
   - It must take a text file path as its first argument.
   - It must output nothing to stdout, but exit with code `0` if the text is CLEAN (real customer) and exit with code `1` if the text is EVIL (bot/spam).
   - You are provided with training data in `/app/corpus/clean/` (contains clean transcripts) and `/app/corpus/evil/` (contains spam transcripts).
   - You must inspect these directories, perform feature engineering (e.g., word frequency analysis, regex pattern matching, or text length thresholds), and tune your bash script's logic until it perfectly separates the two sets. 
   - We will test your `/home/user/filter.sh` against a holdout set (and the provided set) using an automated adversarial verifier.

Requirements:
- Your filter must be written in Bash. You can use standard Unix utilities (grep, awk, sed, wc) inside the script.
- Ensure your scripts have executable permissions.