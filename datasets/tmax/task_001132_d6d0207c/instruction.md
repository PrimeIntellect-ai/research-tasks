You are assisting a mathematical researcher in organizing a multimodal dataset extracted from lecture recordings. You need to handle video processing, large-scale storage organization, and create a robust semantic filter for extracted text snippets.

Part 1: Video Storage Management
1. You have a lecture video located at `/app/dataset_video.mp4`.
2. Extract the frames from this video at exactly 1 frame per second.
3. To manage the storage efficiently, chunk the extracted frames into separate tarballs. Every 5 consecutive frames (e.g., 001 to 005, 006 to 010) must be archived into `chunk_0.tar.gz`, `chunk_1.tar.gz`, etc.
4. Place these chunked tarballs in `/home/user/archive/`. 

Part 2: Text Embedding & Filtering
The researcher has extracted text snippets from various slides, but the OCR process often captures non-mathematical garbage or professor chatter.
1. You are provided with a training/validation dataset:
   - `/app/corpora/clean/` contains text files with valid mathematical theorems.
   - `/app/corpora/evil/` contains text files with OCR garbage and conversational text that must be rejected.
2. We have provided an embedding generator script at `/app/embed.py`. Running `python3 /app/embed.py <text_file>` will print a 10-dimensional numerical vector (space-separated floats) representing the semantic embedding of the file's text.
3. You must write a shell script `/home/user/classifier.sh` that takes a single text file path as an argument.
4. Inside `classifier.sh`, you should call `/app/embed.py`, process the resulting embedding, and compare it (e.g., via cosine similarity) to a reference mathematical embedding. You can compute this reference by averaging the embeddings of the files in `/app/corpora/clean/`.
5. Your script MUST exit with code `0` if the text is classified as valid math (clean), and exit with code `1` if it is classified as garbage/chatter (evil).
6. You must tune your classification threshold so that it perfectly separates the provided `clean` and `evil` directories.

Verification:
An automated test will run your `/home/user/classifier.sh` against a hidden adversarial test set with an identical distribution to evaluate your solution. It requires 100% of the hidden evil corpus to be rejected (exit code 1) AND 100% of the hidden clean corpus to be preserved (exit code 0). 
Ensure your chunked video archives are correctly named and located in `/home/user/archive/`.