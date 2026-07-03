You are an AI assistant helping a data science researcher organize their field datasets. 

The researcher has an audio recording of their field notes located at `/app/research_log.wav`. They also have a set of textual queries they want to look up against these notes, located in `/app/search_queries.txt` (one query per line).

Your task is to build a reproducible pipeline to answer these queries directly from the audio recording. 

Please perform the following steps:
1. **Environment Setup**: Install any necessary Python packages for audio transcription and text embeddings (e.g., `openai-whisper`, `sentence-transformers`, `scikit-learn`, `nltk`).
2. **Transcription**: Write a script to transcribe the `/app/research_log.wav` audio file into text. Using a small, lightweight model (like the `tiny` or `base` whisper model) is recommended to save time.
3. **Tokenization and Preparation**: Clean the transcribed text and segment it into individual sentences (using standard punctuation like '.', '?', '!' as delimiters, or an NLP library).
4. **Embedding and Retrieval**: Compute semantic embeddings for each sentence in the transcript and for each query in `/app/search_queries.txt`. For each query, retrieve the single most semantically similar sentence from the transcribed audio.
5. **Output**: Save your final results to `/home/user/results.json`. The file must be a valid JSON dictionary where the keys are the exact string queries from `/app/search_queries.txt`, and the values are the single best-matching transcribed sentence you retrieved.

You should organize your code into a reproducible pipeline (e.g., a main shell script or Makefile that runs the steps) in `/home/user/pipeline/`.

Your work will be evaluated automatically by comparing your retrieved sentences against the hidden ground-truth segments of the audio corresponding to each query. High semantic similarity to the ground truth is required to pass.