You are a backup administrator for a security camera storage system. Recently, the automated ingestion pipeline has been crashing because it keeps trying to process corrupted or maliciously malformed backup packages. Specifically, some backup packages contain symlink loops that hang our archiving tools, corrupted tar archives, or fake video files that cause our transcoder to panic. 

Your task is to write a Bash script at `/home/user/filter.sh` that acts as a strict ingestion validator. The script must take a single argument: the path to a backup package directory.

The script must exit with `0` (success) if the package is valid and clean. It must exit with a non-zero status (e.g., `1`) to reject the package if any of the following "evil" conditions are met:

1. **Symlink Loops:** The directory contains any symlink loops (e.g., `linkA -> linkB` and `linkB -> linkA`). Your script must reliably detect these without hanging into infinite loops.
2. **Missing or Corrupted Archive:** The directory must contain a file named `payload.tar`. This archive must pass a basic tar integrity check.
3. **Fake Video Files / Invalid Headers:** Extract the `payload.tar` (in a temporary safe location). It will contain a `.mp4` file. You must extract the very first frame of this `.mp4` file as an image. Extract the first 3 bytes (the binary header/magic bytes) of this extracted image. If the bytes do not match the standard JPEG magic number (`FF D8 FF`), the package is invalid and must be rejected.
4. **Known Corrupted Feed Signature:** We have a known corrupted reference video located at `/app/reference_feed.mp4`. Before classifying packages, analyze this reference video to find its exact total frame count. If the `.mp4` inside the backup package has the *exact same frame count* as `/app/reference_feed.mp4`, it is a recurring corrupted feed and must be rejected.

Your script must be written in Bash (`/home/user/filter.sh`) and be marked as executable. It must be self-contained and perform all cleanups of temporary files before exiting, regardless of whether it accepts or rejects the package.