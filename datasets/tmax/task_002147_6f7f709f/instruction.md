You are tasked with implementing a C++ program for bioinformatics sequence processing. We have an audio recording of a senior researcher dictating the baseline parameters for our new sequence scoring model. 

First, locate and transcribe the audio file at `/app/model_parameters.wav`. You can use the `whisper` CLI tool (pre-installed) to transcribe the audio. The recording contains three crucial parameters: `alpha`, `beta`, and `window_size`.

Next, write a C++ program at `/home/user/seq_score.cpp` and compile it to `/home/user/seq_score`. 
Your program must behave as follows:
1. Read a single line of DNA sequence (containing only A, C, G, T) from standard input.
2. Convert the sequence into a numerical signal using the mapping: A=1, C=2, G=3, T=4.
3. Apply a linear transformation to each numerical value using the parameters from the audio: `new_val = (val * alpha) + beta`.
4. Apply a simple moving average filter over the sequence using `window_size`. For the first `window_size - 1` elements where a full window is not available, the average should be computed over whatever elements are available from the start of the sequence up to that point.
5. Output the resulting sequence of values as space-separated integers (truncate the decimal part; do not round).

The compiled executable must handle arbitrary length sequences (up to 10,000 characters) and will be strictly tested against a reference implementation for exact bit-level equivalence on a wide range of inputs.