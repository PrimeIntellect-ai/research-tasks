You are a data analyst and systems engineer. We have lost the source code for a legacy C++ retrieval tool, but we still have the compiled binary (`/app/oracle_finder`), the reference video (`/app/conveyor.mp4`), and our embedding database (`/app/item_embeddings.csv`). 

Your task is to reverse-engineer and rewrite this tool in C++ from scratch so we can modify it in the future. You must compile your tool to `/home/user/finder`.

### Background
The tool performs a multimodal retrieval by joining video features with a CSV database. It operates in a Linux terminal.

### The Logic
We know the legacy tool behaves exactly as follows:
1. It accepts two positional arguments: a frame index (integer, 0-indexed) and a query vector (three comma-separated integers).
   Example invocation: `./finder 42 1500,2000,500`
2. It extracts the specified frame from `/app/conveyor.mp4` (resolution is 640x360). To ensure pixel-exact matching with the legacy tool, you **must** extract the frame's grayscale raw bytes by invoking `ffmpeg` via a subprocess (e.g., using `popen`). The exact `ffmpeg` command you must use to fetch the bytes is:
   `ffmpeg -v error -i /app/conveyor.mp4 -vf "select=eq(n\,<FRAME_INDEX>)" -vframes 1 -pix_fmt gray -f rawvideo -`
3. It reads the raw bytes from `ffmpeg`'s stdout and computes the integer "average brightness" `B`. `B` is defined as the sum of all pixel values (0-255) divided by the total number of pixels (`640 * 360`), using standard integer division (truncation).
4. It reads `/app/item_embeddings.csv`. The CSV has a header and four columns: `ItemID, E1, E2, E3`.
5. For each row in the CSV, it computes a "dynamic embedding" by multiplying the base embedding by the brightness `B`. Thus, the dynamic embedding is `[E1 * B, E2 * B, E3 * B]`.
6. It computes the Manhattan (L1) distance between the query vector `[q1, q2, q3]` and the dynamic embedding.
7. It prints strictly the `ItemID` (a string) of the row with the smallest L1 distance to standard output, followed by a newline. If there is a tie, it picks the row with the lexicographically smallest `ItemID`.

### Requirements
- Ensure any necessary packages (like `ffmpeg`, `g++`) are installed.
- Write your code in `/home/user/finder.cpp`.
- Compile it to `/home/user/finder` using standard C++17.
- Your program's output must be absolutely bit-exact with the legacy tool `/app/oracle_finder` across all edge cases.

Build the environment, write the C++ code, test it locally against the oracle, and leave the compiled binary at `/home/user/finder` when you are done.