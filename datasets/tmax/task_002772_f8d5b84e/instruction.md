You are a Data Engineer building the initial stage of an ETL pipeline that filters unstructured text documents based on their relevance to a target domain.

We have a reference audio recording provided by the data science team, which contains a spoken phrase defining our target domain. You need to transcribe this audio, then build a Python-based filtering script to process text corpora using similarity search.

**Your Tasks:**

1. **Audio Transcription**
   - Transcribe the audio file located at `/app/reference_audio.wav`. You may install and use any standard CLI or Python-based audio transcription tool (e.g., `whisper`, `SpeechRecognition`, etc.).
   - Note the exact spoken phrase, as you will use it as the "reference query" for your similarity filter.

2. **Environment & Pipeline Setup**
   - Install required numerical libraries for feature extraction and similarity search (e.g., `numpy`, `scikit-learn`).
   - Create a Python script at `/home/user/filter_records.py`.
   
3. **Filter Implementation**
   - The script `/home/user/filter_records.py` must accept exactly two arguments using `argparse`: `--input-dir` and `--output-dir`.
   - It should read all `.txt` files inside `--input-dir`.
   - For each file, it must compute a similarity score between the file's text and the **transcribed reference query**.
   - **Algorithm requirements:** Use `scikit-learn`'s `TfidfVectorizer` (with `stop_words='english'`). Fit the vectorizer on a corpus consisting of the reference query AND the current document being evaluated. Compute the `cosine_similarity` between the query vector and the document vector.
   - If the cosine similarity is **greater than 0.05**, the document is considered "relevant" and should be copied into `--output-dir` with its original filename. If it is less than or equal to 0.05, it must be ignored.
   - The script must create the `--output-dir` if it does not exist.

Ensure your Python script is executable and operates cleanly, as it will be tested by an automated test suite against a set of known documents.