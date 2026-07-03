You are a data scientist working on cleaning and analyzing a new voice command dataset. You have received an audio file located at `/app/voice_commands.wav`. We need to extract the spoken words, measure their character lengths, and perform statistical evaluation using bootstrap resampling—all using only standard Bash, Awk, and CLI tools. 

Please perform the following steps:
1. **Environment Setup:** Download and compile `whisper.cpp` in `/home/user/whisper`. Download the `tiny.en` model using their provided script.
2. **Transcription:** Transcribe the audio file `/app/voice_commands.wav` using `whisper.cpp`. Output the transcription to a text file.
3. **Data Cleaning:** Extract just the alphabetical words spoken in the audio. Convert them to lowercase, and remove all punctuation, numbers, and timestamps. Put each word on a new line in `/home/user/clean_words.txt`.
4. **Bootstrap Sampling (Awk/Bash):** We want to estimate the standard error of the mean (SEM) of the word lengths (number of characters per word) in this dataset. 
   Write a Bash/Awk script to perform bootstrap resampling:
   - Sample from the words in `clean_words.txt` *with replacement* to create a bootstrap sample of the same size as the original dataset.
   - Calculate the mean word length of this sample.
   - Repeat this process exactly 5,000 times to get 5,000 bootstrap means.
   - Calculate the standard deviation of these 5,000 means. This value is your Bootstrap SEM.
5. **Reporting:** Create a final file at `/home/user/analysis_report.txt` with exactly two lines:
   `Mean_Length=<actual mean length of words in clean_words.txt>`
   `Bootstrap_SEM=<calculated bootstrap standard error>`

Ensure your bootstrap script relies entirely on standard Linux utilities (e.g., `awk`, `bash`, `shuf`, `bc`). Do not use Python, R, or any other high-level scripting languages for the bootstrap or mean calculations. Round the final numbers in the report to 4 decimal places.