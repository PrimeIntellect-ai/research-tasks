Hello! I am a researcher organizing some speech datasets for an NLP project. We have a pipeline that processes interview recordings, extracts text, and computes feature vectors. Unfortunately, I just realized our current pipeline has a massive data leak: it uses scikit-learn's `fit_transform` on the entire corpus at once, meaning the document frequencies (IDF) for the training data are influenced by the test data!

I need you to build a strictly causal, online ETL pipeline that prevents this.

Here are your tasks:

**Phase 1: Audio Processing**
1. We have an audio recording of an interview located at `/app/dataset/interview.wav`.
2. Use the command-line tool `whisper` (which is pre-installed) to transcribe this audio file. Use the `tiny` model to save time.
3. Extract just the raw transcribed text (ignoring timestamps) and save each transcribed segment as a new line in `/home/user/transcription.txt`.

**Phase 2: The Online Feature Extractor**
To fix the data leak, I need a custom Python script that computes document features in a strictly streaming, online fashion (updating statistics *only* based on currently and previously seen documents).

Create a script at `/home/user/online_tfidf.py`.
It must read documents from standard input (`stdin`), one document per line. For each line, it must print a single floating-point number to standard output (`stdout`), representing the L2 norm of the document's TF-IDF vector, rounded to 4 decimal places.

**Exact Specification for `online_tfidf.py`:**
- **Tokenization:** Convert the line to lowercase. Split by standard whitespace into a list of tokens.
- **State:** The script must maintain a running count of total documents seen so far ($N$) and a mapping of document frequencies for each term ($DF(t)$).
- **Processing order for each document (line):**
  1. Increment the total document count $N$ by 1.
  2. For every *unique* token $t$ present in the current document, increment its document frequency $DF(t)$ by 1. *(Note: updating the DF happens before computing the vector, simulating that the document is added to the known corpus).*
  3. For each unique token $t$ in the document, compute the Term Frequency (TF): 
     $TF(t) = \frac{\text{count of } t \text{ in document}}{\text{total tokens in document}}$
  4. Compute the Inverse Document Frequency (IDF) for each token:
     $IDF(t) = \ln\left(\frac{N}{DF(t)}\right) + 1.0$  *(Use natural logarithm `math.log`)*
  5. The TF-IDF weight for the token is $TF(t) \times IDF(t)$.
  6. Compute the L2 norm (Euclidean length) of the document's TF-IDF vector:
     $L2 = \sqrt{\sum (TF\text{-}IDF(t))^2}$
  7. Print the L2 norm formatted to exactly 4 decimal places (e.g., `0.4512`). If the document has 0 tokens, output `0.0000`.

**Phase 3: Integration**
Run your `online_tfidf.py` script on the `/home/user/transcription.txt` file and redirect the output to `/home/user/features.txt`.

Make sure your script perfectly matches this specification, as I will be running an automated fuzz-tester against it to ensure numerical accuracy and causal correctness.