I am a researcher working with an actively generating dataset, but the proprietary processing software I have aggressively cleans up intermediate data that I actually need for my experiments. 

There is a stripped binary located at `/app/proprietary_processor`. When executed with a target directory (e.g., `/app/proprietary_processor /home/user/workspace`), it rapidly generates a complex, deeply nested directory structure inside `processing/` within the target directory. It writes exactly 1000 intermediate `.dat` files into these random subdirectories. 

The problem: it deletes each `.dat` file mere milliseconds (around 50ms) after writing it, effectively rotating and discarding my data in a race condition. 

Your task is to write a Bash script at `/home/user/rescue.sh` that I can run in the background *before* starting the processor. The script must:
1. Recursively monitor the `/home/user/workspace/processing/` directory (which might not exist until the processor starts).
2. Intercept and save as many of the `.dat` files as possible before the processor deletes them. Save them to `/home/user/rescued_data/`. (Hint: consider filesystem tricks like hard linking to instantly secure the data blocks before the original path is unlinked).
3. Compute the SHA256 checksum of every successfully rescued file.
4. Append these checksums to a manifest file at `/home/user/rescued_data/manifest.txt` in the standard `sha256sum` output format (`<hash>  <filename>`). 

The script must be entirely written in Bash (using standard coreutils, `inotify-tools`, etc.). It should run indefinitely until killed. 

You must create the `/home/user/rescue.sh` script and ensure it is executable. You do not need to run the processor yourself—the automated testing suite will execute your script in the background, run the processor, and then grade your script based on how many unique, intact files were captured in the manifest. You need to capture at least 85% of the 1000 generated files to succeed.