I am a researcher dealing with a continuous stream of sensor data, and I need a reliable way to organize and archive snapshots of my dataset. Currently, my raw sensor logs are stored as individually gzipped files in a directory. 

I need you to write a Rust command-line application that processes these compressed logs and bundles them into a single uncompressed tar archive along with a cryptographic manifest.

Here are the precise requirements for the task:

1. **Input Data**: The input files are located in `/home/user/sensor_data/`. This directory contains several `.csv.gz` files (e.g., `alpha.csv.gz`, `beta.csv.gz`).
2. **Rust Project**: Create a Rust project named `dataset_archiver` in `/home/user/dataset_archiver/`.
3. **Processing Logic**: Your Rust program must:
    - Iterate over all `.csv.gz` files in `/home/user/sensor_data/`.
    - Stream and decompress each file on-the-fly.
    - Calculate the SHA-256 checksum of the **uncompressed** data as it streams.
    - Write the uncompressed data directly into a single new tar archive located at `/home/user/processed_dataset.tar`. The files in the tar archive should have the `.csv` extension (e.g., `alpha.csv`, `beta.csv`).
4. **Manifest Creation**: After all CSV files are added to the tar archive, the program must generate a JSON manifest and append it as a file named `manifest.json` into the root of the same tar archive.
    - The JSON structure must be a single JSON object where the keys are the uncompressed filenames (e.g., `"alpha.csv"`) and the values are their corresponding lowercase hex-encoded SHA-256 checksums. Example:
      ```json
      {
        "alpha.csv": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "beta.csv": "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92"
      }
      ```
5. **Execution**: Once your Rust code is written, build it using `cargo build --release` and execute it to generate the final `/home/user/processed_dataset.tar` file.

Do not delete or modify the original files in `/home/user/sensor_data/`. Your program should gracefully handle standard I/O and rely on popular community crates like `flate2`, `tar`, `sha2`, and `serde_json` if needed.