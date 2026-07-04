You are a machine learning engineer tasked with preparing a training data pipeline for a speech-to-intent model. This involves setting up the environment, extracting tabular features from audio transcripts, and reconstructing an undocumented legacy feature projector.

**Part 1: Audio Feature Extraction**
1. We have an audio recording of a spoken command located at `/app/command.wav`.
2. Install the necessary dependencies to compile and run `whisper.cpp` (a C/C++ port of OpenAI's Whisper). You will need to clone it to `/home/user/whisper.cpp` and download the `tiny.en` model. 
3. Run inference on `/app/command.wav` to generate a word-level timestamped transcript. 
4. Transform this output into a tabular format. Create `/home/user/features.csv` with the headers: `word,start_time_ms,end_time_ms,duration_ms,char_count`. Extract these features for the first 5 words spoken in the audio file.

**Part 2: Feature Projection & Model Output Validation (C Programming)**
Our original training pipeline used a proprietary linear layer to project a 5-dimensional feature vector into a 3-dimensional latent space. We only have the compiled binary left: `/app/oracle_projector`.

1. `/app/oracle_projector` reads exactly 5 space-separated floating-point numbers from standard input (representing a feature vector).
2. It internally applies a linear transformation (a 5x3 matrix multiplication) followed by a ReLU activation function ($max(0, x)$).
3. It prints the resulting 3 floating-point numbers to standard output, each formatted to exactly 4 decimal places, separated by spaces.
4. Your task is to reverse-engineer the underlying 5x3 projection matrix by querying the oracle with basis vectors.
5. Write a C program at `/home/user/project_features.c` that exactly replicates the behavior of `/app/oracle_projector` (same matrix, same activation, identical output format to 4 decimal places). Compile it to `/home/user/project_features`. It will be strictly tested against the oracle for bit-exact equivalence on random floating-point vectors.

**Part 3: Final Integration**
Read the first row of numerical values from your `/home/user/features.csv` (specifically `start_time_ms`, `end_time_ms`, `duration_ms`, `char_count`, and a final padding value of `1.0`). Pass these 5 values as input into your compiled `/home/user/project_features` binary. Save the exact standard output to `/home/user/final_activations.txt`.