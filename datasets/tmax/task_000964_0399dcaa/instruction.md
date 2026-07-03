You are an AI assistant acting as a Machine Learning Engineer. You are preparing training data for a new speech emotion recognition model. The pipeline requires extracting a custom statistical feature called the "Modified Stochastic Energy Contour" (MSEC), plotting the experimental data, and recovering the transcript of the source audio.

You have been provided with an audio recording of an interview at `/app/interview.wav`.

Your task consists of the following steps:

1. **Audio Transcription**
   Install any necessary transcription tools (e.g., `openai-whisper`, `ffmpeg`) and transcribe the audio file `/app/interview.wav`.
   Save the exact raw text of the transcription to `/home/user/transcript.txt`. The text should be purely the transcribed words (no timestamps).

2. **MSEC Feature Extractor (C++)**
   Our current Python implementation of the MSEC feature extractor is too slow for our multi-dimensional array manipulation and Monte Carlo simulation pipeline. You must write a high-performance C++ program to replace it.
   
   Create a C++ file at `/home/user/fast_extractor.cpp` and compile it to an executable at `/home/user/fast_extractor` (ensure it is executable).
   
   **Extractor Specification:**
   * **Input:** Reads a single line of space-separated signed 16-bit integers from standard input (`stdin`). These represent the raw PCM audio samples.
   * **Output:** Prints a single line of space-separated integers to standard output (`stdout`).
   * **Algorithm:**
     1. Read all samples into a 1D array.
     2. Apply sliding window processing: use a window size of $W = 256$ samples and a step (stride) of $S = 128$ samples. Discard any trailing samples that do not form a full window of 256.
     3. For each window $X$, compute the discrete numerical derivative: $D[i] = X[i+1] - X[i]$ for $i = 0, \dots, 254$.
     4. Calculate the base energy via numerical integration of the squared derivative: $E = \sum_{i=0}^{254} (D[i])^2$.
     5. To efficiently approximate our analytical validation model of Gaussian noise injection without floating-point divergence, compute the modified stochastic energy using integer arithmetic: $E_{mod} = (E \times 137) \pmod{999983}$.
     6. Print the $E_{mod}$ values, separated by a single space.

3. **Experimental Data Visualization**
   Write a Python script `/home/user/plot_features.py` that reads the audio file `/app/interview.wav`, converts it to a sequence of 16-bit signed PCM integers, passes them to your `/home/user/fast_extractor` executable, and plots the resulting MSEC feature array.
   Save the visualization to `/home/user/sec_plot.png`. The plot must include a title and labeled axes.

Please proceed with setting up the environment, writing the code, and generating the required files.