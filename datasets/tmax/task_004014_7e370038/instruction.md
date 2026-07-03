You are an artifact manager responsible for curating binary repositories. We have received a new batch of software artifacts in `/app/repo`, but the release manifest was only provided as an audio dictation due to a system glitch.

Your task is to:
1. Process the audio manifest located at `/app/manifest_audio.wav`. You may download and compile transcription tools (like `whisper.cpp`) to transcribe this file. The speaker will list several 3-digit artifact IDs that are "approved" for this release.
2. Write a C++ program (compile it to `/home/user/curate`) that accepts these approved IDs as command-line arguments.
3. For each approved ID, the C++ program must:
    a. Locate the corresponding archive at `/app/repo/artifact_<ID>.tar.gz`.
    b. Verify the archive's integrity (some archives in the repo are known to be corrupted due to incomplete transfers). If an archive is corrupted, safely log it to `/home/user/corruption.log` and skip it.
    c. For valid archives, extract the inner file (it will be named `raw_binary.bin`) into a staging directory `/home/user/staging/`.
    d. To prevent race conditions from other background indexers, you must extract to a temporary filename first (e.g., `.tmp`) and then atomically rename it to `release_<ID>_stable.bin`.
4. After the C++ program completes the extraction and bulk renaming, package the contents of `/home/user/staging/` into a final, highly-compressed archive at `/home/user/curated_release.tar.xz`.

**Evaluation Requirements**:
Our automated test suite will evaluate your final archive using a strict numerical metric: the compressed file size. 
You must use aggressive compression to ensure `/home/user/curated_release.tar.xz` is as small as possible while preserving the correct `release_<ID>_stable.bin` files. The metric is a threshold: `file_size_bytes <= TARGET_SIZE`.