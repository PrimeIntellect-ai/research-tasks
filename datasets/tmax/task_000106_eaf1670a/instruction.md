You are a data analyst tasked with processing an audio search query and finding the most relevant documents in a dataset.

You have been provided with the following files:
1. `/app/query.wav`: An audio recording of a user's search query.
2. `/app/vocab.csv`: A comma-separated file mapping words to their 5-dimensional embeddings. Format: `word,v1,v2,v3,v4,v5`.
3. `/app/documents.csv`: A comma-separated file containing document IDs and their 5-dimensional embeddings. Format: `doc_id,v1,v2,v3,v4,v5`.

Your workflow must be implemented entirely using Bash, standard shell utilities (like `awk`, `sed`, `grep`), and any open-source CLI tools you download and compile (e.g., `whisper.cpp` for audio transcription). Do not use Python, R, or other high-level scripting languages for the data processing or math.

Step 1: Audio Transcription
Install a suitable CLI tool (we recommend compiling `whisper.cpp` from source and downloading the `tiny.en` model) to transcribe `/app/query.wav`. Extract the transcribed text, convert it to lowercase, and remove any punctuation.

Step 2: Query Embedding Computation
For each word in the normalized transcription, look up its embedding in `/app/vocab.csv`. 
Compute the query embedding by calculating the element-wise sum of the embeddings of all words in the query. (If a word is missing from the vocabulary, ignore it).

Step 3: Document Retrieval
Using `awk` or another shell utility, compute the Cosine Similarity between your summed query embedding and every document embedding in `/app/documents.csv`.
Sort the documents by their similarity score in descending order.

Step 4: Output
Save the top 10 results to `/home/user/results.csv`. 
The file must have exactly this format (no header):
`doc_id,similarity_score`
Round the similarity scores to 4 decimal places.

Ensure your environment setup, processing, and mathematical computations are robust and reproducible.