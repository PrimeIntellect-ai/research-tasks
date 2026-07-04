You are an artifact manager responsible for curating our video binary repositories. We have received a new raw video artifact at `/app/artifact_feed.mp4`. Your task is to optimize this video and integrate it into our repository file structure using a Bash script.

Perform the following steps:
1. Write a Bash script (or run commands) to compress `/app/artifact_feed.mp4` using `ffmpeg` and save the result as `/home/user/optimized_artifact.mp4`. 
   - **Constraint**: The final optimized file must be less than exactly 2,000,000 bytes in size.
   - **Quality**: You must maximize the visual quality. An automated verifier will check the Structural Similarity Index (SSIM) between your optimized video and the original. Your video must achieve an overall SSIM of >= 0.92.

2. Parse the configuration file at `/app/repo_layout.conf`. This file dictates how the artifact should be linked into the repository hierarchy. The file has the following format:
   ```
   BASE_DIR=/home/user/repository
   PRIMARY_LOCATION=releases/v2.0/main_artifact.mp4
   HARD_LINKS=stable/latest.mp4,promoted/v2.mp4
   SYM_LINKS=experimental/beta.mp4
   ```
   You must:
   - Create the necessary directory structure under the specified `BASE_DIR`.
   - Move or copy your `/home/user/optimized_artifact.mp4` to the `PRIMARY_LOCATION` (relative to `BASE_DIR`).
   - Create hard links for the paths listed in `HARD_LINKS` (relative to `BASE_DIR`) pointing to the primary location.
   - Create symbolic links for the paths listed in `SYM_LINKS` (relative to `BASE_DIR`) pointing to the primary location. Symlinks should use relative paths to point to the target to ensure the repository remains portable if moved.

Ensure all directories, files, and links exist exactly as specified in the configuration file once you are done.