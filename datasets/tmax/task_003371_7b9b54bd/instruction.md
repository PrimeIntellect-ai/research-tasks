You are a performance engineer tasked with profiling and fixing a vulnerability in our bioinformatics genetic optimization pipeline. The pipeline currently crashes with a core dump during matrix factorization when it encounters near-singular inputs. 

The lead scientist left an audio recording detailing the exact mathematical conditions of the anomaly and how to build a pre-filter, but they are currently on leave.

Your objectives:
1. Recover the exact filtering conditions by transcribing the audio file located at `/app/issue_report.wav`.
2. Write a Rust command-line application in `/home/user/sequence_filter` that acts as a robust filter.
3. The application must accept a single command-line argument: a path to a directory containing `.fasta` files.
4. For each file in the directory, it must output exactly one line to `stdout` in the format: `filename.fasta,STATUS` where `STATUS` is either `CLEAN` or `EVIL`.
5. You are provided with two corpora of `.fasta` files to test your filter:
   - `/app/corpus/evil/`: Contains files known to cause the matrix factorization crash. Your filter MUST classify 100% of these as `EVIL`.
   - `/app/corpus/clean/`: Contains typical sequences. Your filter MUST classify 100% of these as `CLEAN`.

You may use any transcription tools (e.g., Python `openai-whisper`, `ffmpeg`) to process the audio, and any Rust crates (e.g., `rand`, `statrs`) to implement the Monte Carlo and probability metric calculations described in the audio.

Once your Rust binary is compiled and working perfectly against both corpora, leave it at `/home/user/sequence_filter/target/release/sequence_filter` so the automated validation suite can test it.