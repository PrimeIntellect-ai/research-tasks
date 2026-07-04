You are a data scientist tasked with cleaning a dataset of customer service voice memos and their corresponding transcripts. We are facing a wave of adversarial spam and prompt-injection attacks through our voice channels. 

Your goal is to build a reproducible pipeline in Bash that classifies transcripts as either "clean" (legitimate customer requests) or "evil" (malicious attacks/spam).

You have been provided with the following files:
1. **Audio Briefing**: `/app/voicemail.wav` - An audio message left by the lead security engineer. You must transcribe this audio to discover two critical, hardcoded rules for identifying malicious actors.
2. **Training Transcripts**: `/app/train/transcripts/` - A directory containing `.txt` files. The filename is the `transcript_id` (e.g., `user_102.txt`).
3. **Training Metadata**: `/app/train/metadata.csv` - A CSV file containing `transcript_id,ip_address,account_age_days,duration_seconds`.
4. **Training Labels**: `/app/train/labels.csv` - A CSV mapping `transcript_id` to label (`clean` or `evil`). 

**Instructions:**
1. **Feature Engineering & Selection**: Analyze the training data. Beyond the rules mentioned in the audio briefing, there is one additional text-based pattern common to the `evil` training transcripts that does not appear in the `clean` ones. You must discover this pattern.
2. **Multi-source Data Joining**: Your classification logic must inspect both the text of the transcript and the metadata associated with its `transcript_id`.
3. **Pipeline Construction**: Create a robust Bash script at `/home/user/filter.sh`. 

**Execution Signature:**
Your script must accept exactly two arguments:
`./filter.sh <path_to_transcript.txt> <path_to_metadata.csv>`

For example:
`./filter.sh /app/train/transcripts/user_102.txt /app/train/metadata.csv`

**Expected Behavior:**
- The script must extract the `transcript_id` from the filename (e.g., `user_102`).
- It must look up the corresponding metadata row in the provided CSV.
- It must apply the classification rules (the two from the audio, plus the one you discovered from the training data).
- **Exit Code**: The script must exit with status `0` if the transcript is `clean` (accept), and exit with status `1` if it is `evil` (reject).
- Ensure your script is executable (`chmod +x /home/user/filter.sh`).

You may use standard Linux utilities (`grep`, `awk`, `sed`, `jq`) and invoke Python scripts if needed for transcription or complex text processing, but the main entry point MUST be your Bash script.