You are a machine learning engineer preparing training data for a new bioinformatics foundation model. Part of your pipeline requires a lightning-fast feature extraction tool written in C to process genomic data.

An audio file containing the specifications for this feature extractor was left by the lead bioinformatician at `/app/instruction.wav`. 

Your task:
1. Transcribe or listen to the audio file `/app/instruction.wav` to understand the algorithm requirements. (You may use any available tools in the environment to transcribe this audio, such as `whisper` or Python libraries).
2. Implement the feature extractor in C. Save your source code at `/home/user/extractor.c`.
3. Compile your code to an executable at `/home/user/extractor`.

The executable `/home/user/extractor` must read data from standard input (stdin) and print the requested features to standard output (stdout). 
It must be robust to various inputs as it will be rigorously tested against thousands of randomly generated sequences by our continuous integration system to ensure it is bit-exact equivalent to a reference implementation.

Please leave the compiled executable at `/home/user/extractor` when you are finished.