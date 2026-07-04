You are a bioinformatics analyst working with a prototype nanopore sequencer that outputs raw electrical current measurements encoded as audio files. We have a test recording located at `/app/nanopore_signal.wav`. 

Your goal is to build a Go-based processing pipeline that analyzes this audio signal, performs spectral analysis, and decodes it into a DNA sequence.

Here is what we know about the sequencer's signal:
- The signal is a mono, 16-bit PCM WAV file with a sample rate of 8000 Hz.
- Each nucleotide base pair takes exactly 0.1 seconds to pass through the pore.
- The sequencer emits a specific frequency for each nucleotide:
  - **A**: ~440 Hz
  - **C**: ~550 Hz
  - **G**: ~660 Hz
  - **T**: ~770 Hz
- The signal contains some background noise.

Your tasks:
1. Write a Go program at `/home/user/decoder.go` that reads `/app/nanopore_signal.wav`.
2. Process the audio in sliding windows of 0.1 seconds (800 samples). Use Go's concurrency features (goroutines) to process multiple windows in parallel.
3. For each window, compute the Fast Fourier Transform (FFT) to determine the dominant frequency. You may use a third-party Go FFT library (e.g., `github.com/mjibson/go-dsp/fft`) by initializing a Go module.
4. Map the dominant frequency to the closest nucleotide (A, C, G, or T).
5. Output the reconstructed DNA sequence in standard FASTA format to `/home/user/decoded.fasta`. The sequence header should be `>sequence_1`.

Ensure your Go code is fully self-contained (aside from standard or fetched third-party libraries) and compiles successfully. We will evaluate the accuracy of your decoded sequence against the true underlying DNA sequence using a sequence alignment metric.