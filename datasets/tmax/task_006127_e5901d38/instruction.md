I am a researcher working with a large, messy dataset that was scraped from various sensors. The raw dataset is located at `/home/user/raw_dataset`. It contains many nested subdirectories with files in different formats, but I am only interested in the `.txt` and `.dat` files.

I need you to process this dataset and prepare it for my analysis pipeline. Please perform the following steps:

1. Recursively traverse the `/home/user/raw_dataset` directory and read all `.txt` and `.dat` files.
2. Extract all lines that begin exactly with the string `"DATA: "` (including the space).
3. From these extracted lines, strip out the `"DATA: "` prefix so only the remaining payload is kept.
4. Filter out and discard any of these lines that contain the exact uppercase word `"CORRUPT"` anywhere in the payload.
5. Merge all the valid, cleaned payloads into a single collection. The order in which files are processed does not matter, but all valid lines must be collected.
6. Split this merged collection into smaller chunk files, with exactly 500 lines per file (the last file may have fewer than 500 lines).
7. Save these chunk files in a new directory called `/home/user/processed_dataset/`. Name them sequentially as `dataset_chunk_000.txt`, `dataset_chunk_001.txt`, `dataset_chunk_002.txt`, etc.
8. Finally, create a compressed gzip tar archive of the processed dataset directory at `/home/user/final_dataset.tar.gz`. The archive should contain the files directly or within a `processed_dataset` folder.

Please write a script or use command-line tools to accomplish this task. Once you are finished, I should see `/home/user/final_dataset.tar.gz` containing the correctly chunked data files.