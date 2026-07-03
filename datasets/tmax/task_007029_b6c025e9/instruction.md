You are assisting a researcher who needs to organize a messy dataset for analysis. The raw data is located in `/home/user/raw_data/` and contains various subdirectories with a mix of `.csv` dataset files, `.jpg` images, and `.tmp` junk files. 

Your task is to create a flattened, curated "view" of only the `.csv` files using symbolic links, and then generate a cryptographic manifest of the curated data.

Please perform the following steps:
1. Create a new directory at `/home/user/curated_dataset/`.
2. Find all `.csv` files within `/home/user/raw_data/` (including all subdirectories).
3. For each `.csv` file found, create a symbolic link inside `/home/user/curated_dataset/` that points to the original file's absolute path. The name of the symbolic link must exactly match the original filename (you can assume all `.csv` filenames in the raw dataset are unique).
4. Generate a JSON manifest file at `/home/user/curated_dataset/manifest.json`. The JSON file must be a single dictionary mapping the filename to an object containing its symlink path, original absolute path, and SHA-256 checksum of the file contents.

The `manifest.json` file must strictly follow this exact structure:
```json
{
  "sensorA.csv": {
    "symlink_path": "/home/user/curated_dataset/sensorA.csv",
    "original_path": "/home/user/raw_data/session1/sensorA.csv",
    "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
  },
  "sensorB.csv": {
    ...
  }
}
```

You may use Bash or write a Python script to accomplish this. Ensure your final JSON file is properly formatted and valid.