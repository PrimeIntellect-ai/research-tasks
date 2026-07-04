I'm working on a data pipeline for training an audio-language model, and I need your help preparing the training data processing scripts.

First, I have an audio sample located at `/app/audio_sample.wav`. Please transcribe this audio file. The audio contains a description of a specific text-cleaning rule regarding how missing values or anomalous integers should be handled in our text pipeline (specifically handling cases where missing tokens might introduce unexpected type shifts, similar to pandas converting ints to floats).

Once you've transcribed the audio and understood the rule, you need to create a Bash script at `/home/user/tokenizer.sh`.

This script must:
1. Accept a single string of text as its first argument.
2. Tokenize the text into individual words (split by spaces).
3. Apply the specific cleaning/tokenization rule described in the audio file.
4. Output the final tokens, one per line.

Your script will be tested against a hidden reference implementation using hundreds of random string inputs to ensure it behaves exactly the same (bit-exact equivalence). Make sure your script handles empty strings, special characters, and multiple spaces correctly according to standard Bash text processing, applying the audio's rule precisely.

Please ensure the script is executable (`chmod +x /home/user/tokenizer.sh`).