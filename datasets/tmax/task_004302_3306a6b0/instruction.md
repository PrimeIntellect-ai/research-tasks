I am a researcher organizing a new audio dataset for a machine learning project. I have a long audio recording located at `/app/interview.wav` that I need to process. 

I need you to build a Bash-based ETL pipeline that does the following:
1. Write a Bash script `/home/user/pipeline.sh` that splits the audio file `/app/interview.wav` into 15-second chunks (saving them in `/home/user/chunks/`).
2. The script should then transcribe each audio chunk using a speech-to-text model (you can install and use `openai-whisper` via pip, using the `tiny` model for speed).
3. The script must compile the transcriptions into a single CSV file at `/home/user/dataset.csv`. The CSV should have no header and two columns: the chunk filename (e.g., `out000.wav`) and the transcribed text.
4. I have a Python script at `/home/user/plot_words.py` that is supposed to read `dataset.csv` and generate a bar chart of the top 10 most frequent words, saving it to `/home/user/word_freq.png`. However, the script is currently misconfigured (it crashes or produces blank plots due to a matplotlib backend issue). Please debug and fix `/home/user/plot_words.py` so that it successfully outputs the image in our headless Linux environment.
5. Run your pipeline and the plotting script so that both `/home/user/dataset.csv` and `/home/user/word_freq.png` are generated.

Ensure your Bash script is robust and correctly handles the data transformations. The transcription doesn't need to be perfect, but it must capture the majority of the spoken words correctly (we will evaluate the Word Error Rate).