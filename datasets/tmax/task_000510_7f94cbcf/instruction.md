You are a storage administrator tasked with managing a severely bloated disk partition. A massive influx of redundant data and uncompressed media has caused the `/app/storage_pool` directory to consume too much space. Your objective is to deduplicate the filesystem, generate a cryptographic manifest, and carefully compress a large audio artifact without losing too much fidelity.

Perform the following steps:

1. **Deduplication via Hard Links**:
   The directory `/app/storage_pool` contains hundreds of files, many of which are exact duplicates (both text logs and large audio files). Write a script in a language of your choice to traverse this directory, identify files with identical content (using checksums), and replace all duplicates with **hard links** to a single canonical copy. This will drastically reduce disk usage while keeping all file paths intact.

2. **Manifest Generation**:
   After deduplication, generate a manifest file at `/home/user/dedup_manifest.txt`. The manifest must contain exactly one line per unique file (inode) in `/app/storage_pool`. The format for each line must be:
   `<SHA256_CHECKSUM>  <PATH_TO_ONE_CANONICAL_COPY>`
   Sort the file alphabetically by the file paths.

3. **Audio Compression**:
   You will notice that one large audio file was duplicated many times across the storage pool. The original file is also provided at `/app/voicemail.wav` for reference. 
   As a storage admin, you need to archive this file efficiently. Compress `/app/voicemail.wav` and save it to `/home/user/compressed_audio.ogg`. 
   
   **Constraints**:
   - The final size of `/home/user/compressed_audio.ogg` must be less than 150 KB.
   - You must maintain the highest possible audio quality. Our automated verifier will measure the Mean Squared Error (MSE) between the waveform of your compressed `.ogg` file and the original `.wav` file. 
   - You must achieve an MSE metric of **0.005 or lower**.

You may install any standard packages (like `ffmpeg`, `sox`, or language-specific libraries) needed to achieve this.