We are preparing a large-scale speech dataset for training an automatic speech recognition (ASR) model. Unfortunately, we suspect that a malicious actor has poisoned some of the audio files with a subtle adversarial watermark. This watermark is largely imperceptible to human ears but severely degrades the model's training convergence. 

As our Machine Learning Engineer, you need to build a detection tool to filter out these poisoned files. 

Here is what you have:
- A known clean audio file: `/app/reference_clean.wav`
- A known poisoned audio file: `/app/reference_evil.wav`

Your task:
1. Orchestrate an analysis workflow (you can use Python or Go in a script or interactive session) to analyze the spectral properties of these two reference WAV files. You will need to use Fourier transforms to inspect their frequency domains. 
2. Identify the specific spectral anomaly (e.g., a hidden frequency spike, abnormal variance, or artificial statistical signature) present in the poisoned file but absent in the clean file. Apply statistical hypothesis comparison if necessary to find the distinguishing feature.
3. Once you understand the watermark's signature, write a standalone detector in **Go**. The source code must be saved at `/home/user/detector.go` and compiled to an executable at `/home/user/detector`.
4. Your compiled Go executable must take exactly one command-line argument: the absolute path to a WAV file to be tested.
   - Example invocation: `/home/user/detector /path/to/audio.wav`
5. The detector must return an **exit status of 0** if the audio is clean (acceptable for training), and an **exit status of 1** if the audio contains the adversarial watermark (poisoned).

The automated verification system will run your compiled `/home/user/detector` against two hidden datasets: a corpus of clean audio and a corpus of poisoned audio. To pass, your detector must achieve 100% accuracy: correctly accepting all clean files and rejecting all poisoned files.

Ensure your Go program properly parses WAV file headers and handles the audio data accurately before computing the FFT or statistical checks. You may install and use third-party Go packages (e.g., for WAV parsing or FFT) as needed.