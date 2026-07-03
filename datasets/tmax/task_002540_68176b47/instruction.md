You are tasked with recovering our system's configuration state after a massive unauthorized drift event. As the configuration manager, you must track down when the changes occurred, identify the affected files, and write a highly optimized patcher to revert the changes.

We have a video feed from our configuration dashboard: `/app/config_dashboard_feed.mp4`. Whenever a rogue automated process modified our configuration, the dashboard flashed a pure red square (RGB: 255, 0, 0) in the top-left 50x50 pixels for exactly one frame. The video is at 30 FPS.

We also have a massive backup archive: `/app/config_backups.tar.gz`. It contains a nested directory structure of configuration files.

Your objectives:
1. **Video Analysis**: Use `ffmpeg` and Python to extract and analyze the frames of `/app/config_dashboard_feed.mp4`. Identify the exact frame numbers where the red alert square appears.
2. **Archive & Traversal**: Extract `/app/config_backups.tar.gz` to `/home/user/configs/`. The archive contains thousands of `.conf` files. 
3. **Correlation**: For every frame number `F` identified in step 1, find the file named `config_batch_<F>.conf` within the extracted directories.
4. **Fast Patcher Implementation**: The rogue process injected a massive amount of bloat. You must write a highly optimized Python script at `/home/user/fast_patch.py`.
   - The script must accept a directory path as its first argument.
   - It must recursively traverse the directory and find all `.conf` files.
   - For each file, it must replace every occurrence of the string `[ROGUE_OVERRIDE_ENABLED=TRUE]` with `[SECURE_DEFAULT_LOCKED]`.
   - **Crucial Constraint**: Our production logs are several gigabytes in size. Your script must be incredibly fast. You are strongly expected to use memory-mapped I/O (`mmap`) or highly optimized streaming text edits rather than reading entire files into standard strings or doing line-by-line reads. 
5. **Execution**: Run your patcher on the `/home/user/configs/` directory. Then, compress the corrected directory back into an archive at `/home/user/restored_configs.tar.gz`.

Your final script `/home/user/fast_patch.py` will be tested against a massive 5GB test configuration file by an automated verifier to ensure it meets strict performance thresholds compared to a naive Python implementation.