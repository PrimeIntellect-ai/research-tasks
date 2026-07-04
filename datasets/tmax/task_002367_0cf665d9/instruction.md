You are acting as a technical writer's assistant. The writer creates documentation by extracting keyframes from software tutorial screen recordings.

Your task is to create an automated Bash workflow that processes these tutorial videos.

1. Create a script at `/home/user/process_video.sh` that takes a video file path as its first argument.
2. The script must extract exactly 10 frames from the video, representing the content at exactly 10%, 20%, 30%, 40%, 50%, 60%, 70%, 80%, 90%, and 99% of the total video duration.
3. The script must bulk rename these extracted frames into a strict sequence: `fig_01.jpg`, `fig_02.jpg`, ..., `fig_10.jpg`.
4. The script must generate a manifest file named `manifest.sha256` containing the SHA256 checksums of the 10 images.
5. The script must package the 10 images and the manifest into an archive named `<video_basename>_assets.tar.gz` (e.g., if the input is `tutorial.mp4`, the archive should be `tutorial_assets.tar.gz`) and place this archive in `/home/user/processed/`.
6. Run your script on the provided video fixture: `/app/tutorial.mp4`. Ensure the final archive `/home/user/processed/tutorial_assets.tar.gz` is created successfully.

You will need to ensure all directories are created appropriately. Use `ffmpeg` for the video extraction. Ensure the extracted frames accurately reflect the specified timestamp percentages.