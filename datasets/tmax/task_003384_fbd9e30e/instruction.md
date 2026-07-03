You are a Machine Learning Engineer preparing a large-scale audio dataset for an acoustic model. To reduce data dimensionality and extract specific embeddings, we need a high-performance, memory-efficient feature extraction CLI tool written in Rust. 

Your task is to write this tool and process a sample audio fixture provided in the environment.

**Step 1: Audio Preprocessing**
There is an audio file at `/app/voice_sample.wav`. Convert this file to a raw, 16kHz, mono, 32-bit floating-point (little-endian) PCM stream and save it to `/home/user/sample.bin`. You may use `ffmpeg` for this.

**Step 2: Rust Feature Extractor (Linear Algebra & Storage Optimization)**
Create a Rust project at `/home/user/extractor`. The program must compile to a binary that accepts exactly two arguments: an input file path and an output file path.
Usage: `./target/release/extractor <input.bin> <output.bin>`

The input file will contain continuous raw `f32` (little-endian) PCM samples. Your tool must process the data in a streaming fashion, as it will be used on continuous data streams exceeding 100GB in production. Do not load the entire file into memory at once.

For the transformation logic, implement the following:
1. Read the input `f32` samples sequentially.
2. Group the samples into chunks of exactly 64 samples. If the last chunk is incomplete (less than 64 samples), pad the remainder of the chunk with zeros.
3. Treat each chunk as a 1x64 row vector. Multiply this vector by a 64x128 projection weight matrix to produce a 1x128 vector. 
4. The weight matrix is provided at `/app/projection_matrix.bin` (which contains exactly 8192 `f32` little-endian values in row-major order: row 0 col 0, row 0 col 1, ..., row 63 col 127). You may load this entire matrix into memory at startup.
5. Apply a ReLU activation function ($f(x) = \max(0, x)$) to all 128 elements of the resulting vector.
6. Calculate the arithmetic mean of the 128 elements.
7. Write this single `f32` mean value to the output file (in little-endian format). Repeat this for every chunk.

**Step 3: Processing & Benchmarking**
Run your compiled, release-mode extractor on `/home/user/sample.bin`, and save the output to `/home/user/sample_features.bin`.

Ensure your tool correctly implements the math exactly as described, as it will be tested against a heavily fuzzed oracle implementation using arbitrary byte streams to guarantee bit-exact equivalence.