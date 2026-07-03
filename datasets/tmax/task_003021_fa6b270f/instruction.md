You are a data engineer building an ETL pipeline that processes user-submitted voice commands. Recently, our system has been targeted by adversarial audio attacks where hidden commands (like "delete database") are embedded in otherwise normal sounding audio. 

Your task is to build a C-based classification tool that detects and rejects these adversarial audio files.

Here is what you have:
1. A reference audio file at `/app/reference_sample.wav`.
2. A local clone of `whisper.cpp` located in `/app/whisper.cpp/` and a base model at `/app/models/ggml-base.en.bin`.
3. A pre-trained logistic regression model weights file at `/app/model_weights.csv`. The file contains a list of token hashes and their corresponding regression weights. Bias is 0.
4. Two corpora of audio files for testing: `/app/corpus/clean/` (normal commands) and `/app/corpus/evil/` (adversarial commands).

You must write a C program located at `/home/user/detector.c` and compile it to `/home/user/detector`. 

Your `detector` program must:
1. Accept a single command-line argument: the absolute path to a WAV file.
2. Invoke `whisper.cpp` to transcribe the audio file. You may need to tune the whisper inference hyperparameters (e.g., beam size, temperature) to reliably recover the hidden text in the noisy adversarial files.
3. Tokenize the resulting transcript by splitting on whitespace and converting to lowercase.
4. Compute a simple hash for each token: sum of ASCII values of the characters.
5. Apply the logistic regression model: sum the weights of the token hashes present in the transcript. If the sum is > 0.5, it is classified as evil.
6. The program must return exit code `0` if the audio is clean, and exit code `1` if the audio is evil.

You should test your compiled `/home/user/detector` against the `/app/corpus/clean/` and `/app/corpus/evil/` directories to ensure 100% accuracy.