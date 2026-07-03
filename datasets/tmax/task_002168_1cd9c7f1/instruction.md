You are tasked with cleaning a dataset of incoming audio transcriptions for our machine learning pipeline. We have discovered that some transcriptions are severely corrupted or conceptually out-of-domain (acting as "adversarial" noise). 

We have a golden reference audio file located at `/app/reference.wav`. This file contains the exact topic and tone we expect from a pristine, clean dataset.

Your objective is to build a robust detector that flags incoming text files as either `CLEAN` or `EVIL` (out-of-domain/corrupted).

Here are the specific steps you must take:
1. **Transcribe the Audio**: Extract the spoken text from `/app/reference.wav`. You may set up a Python environment and install any necessary libraries (e.g., `SpeechRecognition`, `pydub`, `sentence-transformers`).
2. **Compute Embeddings**: Using the `all-MiniLM-L6-v2` model from the `sentence-transformers` library, compute the vector embedding of the golden reference transcription. 
3. **Linear Algebra for Anomaly Detection**: For any incoming text, compute its embedding using the same model. Then, calculate its orthogonal rejection from the golden reference embedding (i.e., the component of the incoming embedding that is strictly orthogonal to the reference embedding).
4. **Determine the Threshold**: You are provided with a small calibration dataset in `/home/user/train_clean/` and `/home/user/train_evil/` containing text files. Compute the L2 norm (magnitude) of the orthogonal rejection for these files. Use these values to find a numerical threshold $\tau$ that perfectly separates the clean files from the evil ones.
5. **Create the Classifier**: Write a Python script at `/home/user/detector.py`. The script must take exactly one argument (the path to a text file). It must print exactly `CLEAN` to standard output if the file's orthogonal rejection norm is $\le \tau$, and print exactly `EVIL` if it is $> \tau$.

An automated test suite will evaluate your `/home/user/detector.py` against a hidden adversarial corpus and a hidden clean corpus.

Ensure your environment is correctly configured and that your script executes cleanly, outputting only the required classification.