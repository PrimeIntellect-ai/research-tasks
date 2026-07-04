I am a researcher organizing a dataset of mathematical lecture notes. Unfortunately, our document pipeline got corrupted, and many unrelated or nonsensical text files were mixed into our dataset of linear algebra notes. 

We have a reference audio recording of the core lecture topic at `/app/audio/lecture.wav`.

I need you to build a semantic dataset filter. Please write a Python script at `/home/user/dataset_filter.py` that decides whether a given text file is semantically relevant to the core topic discussed in the audio.

Your script must meet the following specifications:
1. **Command Line Interface**: The script must accept exactly one argument, the path to a text file.
   Usage: `python /home/user/dataset_filter.py <path_to_text_file>`
2. **Audio Transcription**: The script should transcribe the audio file `/app/audio/lecture.wav`. You can use the `openai-whisper` package (the `base` model is sufficient).
3. **Embedding Computation**: Use the `sentence-transformers` library (specifically the `all-MiniLM-L6-v2` model) to compute the embeddings of both the transcribed audio text and the text contained in the input file.
4. **Validation/Filtering**: Compute the cosine similarity between the two embeddings. 
   - If the similarity is **>= 0.40**, print exactly `ACCEPT` to standard output and exit with status code `0`.
   - If the similarity is **< 0.40**, print exactly `REJECT` to standard output and exit with status code `1`.

You will need to set up your own Python environment, install necessary dependencies (like `torch`, `openai-whisper`, `sentence-transformers`, `ffmpeg-python`, etc.), and ensure the script works robustly. You can test your script on any sample text you create. Once you are done, simply leave the script at `/home/user/dataset_filter.py`.