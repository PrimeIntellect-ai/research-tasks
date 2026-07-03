As an artifact manager for our organization's air-gapped environment, you are tasked with recovering a curated binary repository that was transmitted to us via an unconventional channel. To bypass certain firewall restrictions, the upstream team encoded the binary artifact's chunks into QR codes and compiled them into a video stream.

The video artifact is located at: `/app/artifact_feed.mp4`

Your objective is to:
1. Prepare your environment to process the video and extract the frames.
2. Read the QR codes from the extracted frames. The QR codes contain base64 encoded chunks of a `.tar.gz` archive. 
3. Some frames might have duplicated data or corrupt read headers. You must clean the extracted text (using tools like sed/awk) to strip any scanner prefixes (e.g., "QR-Code:") and merge the chunks sequentially based on the video timeline.
4. Reconstruct the original binary archive and save it exactly at `/home/user/recovered_artifact.tar.gz`.
5. Extract the archive into `/home/user/repo/`.
6. Perform a metadata-based search within `/home/user/repo/` to locate all files larger than 10KB that were created before the year 2023. Concatenate their names (sorted alphabetically) into a file located at `/home/user/legacy_binaries.txt`.

We will evaluate the integrity of your recovered binary archive. Ensure that your final recovered archive at `/home/user/recovered_artifact.tar.gz` is bit-for-bit accurate to the maximum extent possible.