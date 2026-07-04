You are tasked with recovering the configuration state of a legacy system right before a critical crash. The only surviving artifacts are a deeply nested set of incremental backups and a video screen recording of the system's stability metrics.

You must build a Rust-based tool at `/home/user/config_manager` (a standard Cargo project) to automate this recovery workflow.

**Phase 1: Video Analysis (The Trigger Frame)**
A video at `/app/stability.mp4` contains 500 frames. The video shows a white square (the "stability indicator") moving vertically on a black background. 
1. Use Rust (you may invoke `ffmpeg` via standard library commands to extract frames) to analyze the video.
2. Identify the frame index (0-indexed) where the white square reaches its *lowest* point on the screen (highest Y coordinate). Let this frame index be `N`. 
`N` represents the revision number of the configuration right before the crash.

**Phase 2: Nested Archive Extraction & Streaming**
The directory `/app/archives/` contains hundreds of zip files named `rev_0.zip`, `rev_1.zip`, up to `rev_499.zip`. Each zip contains a tarball, which in turn contains a set of text files representing incremental updates to the configurations.
1. Your Rust program must sequentially extract the nested archives from `rev_0.zip` up to and including `rev_<N>.zip`.
2. Extract the files into `/home/user/extracted_configs/`. Overwrite files with the same name, mimicking an incremental backup restoration.

**Phase 3: Bulk Renaming and Deduplication**
Within `/home/user/extracted_configs/`, many files have a suffix indicating their module (e.g., `network.conf.mod1`, `database.conf.mod2`).
1. Traverse the directory recursively.
2. Rename all files by stripping the `.modX` suffix (e.g., `network.conf.mod1` becomes `network.conf`). If a file with the new name already exists, append the contents of the newer file to the existing file and delete the newer file.

**Phase 4: Custom RLE Compression**
To minimize storage, you must package the final renamed configuration files into a single custom binary archive at `/home/user/final_state.dat` using your Rust tool.
1. Concatenate all final files in alphabetical order by their absolute path.
2. Compress the concatenated byte stream using basic Run-Length Encoding (RLE):
   - For every sequence of identical bytes, write two bytes: `[count as u8]` followed by `[byte value]`.
   - The maximum `count` is 255. If a sequence exceeds 255, split it into multiple RLE pairs.
   - Example: 300 'A's becomes `[255]['A'][45]['A']`.

**Constraints & Verification:**
- You MUST use Rust for the core logic (video frame analysis, archive traversal, renaming, and RLE compression).
- The success of your task will be evaluated by measuring the byte size of `/home/user/final_state.dat`. You must achieve an output size below a specific threshold (which implies you correctly stopped at revision `N` and correctly applied the RLE scheme).