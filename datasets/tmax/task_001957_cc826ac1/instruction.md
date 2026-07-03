You are assisting a computer vision researcher in organizing a dataset derived from a video experiment. The researcher needs a robust, high-performance pipeline to extract video frames, rename them in bulk, and distribute them into train and validation sets using symbolic and hard links to save disk space.

Your task has three phases:

**Phase 1: Frame Extraction**
Extract frames from the video file located at `/app/experiment_run.mp4`. 
- Use `ffmpeg` to extract frames at exactly 5 frames per second.
- Save the extracted frames into the directory `/home/user/raw_frames/`.
- Name the frames sequentially using a 6-digit zero-padded format (e.g., `000001.jpg`, `000002.jpg`, etc.).

**Phase 2: The Organizer Program (C++)**
The researcher previously used a proprietary tool to determine how frames should be renamed and linked, located at `/app/reference_organizer`. You need to write a C++ replacement that perfectly matches its output behavior.

Write a C++ program at `/home/user/organizer.cpp` and compile it to `/home/user/organizer`. 
The program must read relative file paths from standard input (one per line) and print the classification and link action to standard output.
The logic must be as follows:
1. Parse the input string, which will look like: `[optional_subdirs/]<6-digit-number>.jpg` (e.g., `cam_top/000145.jpg` or `000005.jpg`).
2. Extract the numeric frame ID.
3. If the frame ID is divisible by 5, it goes to the validation set. 
   - Print exactly: `ACTION: HARDLINK, TARGET: val_set/val_<original_filename>`
4. If the frame ID is NOT divisible by 5, it goes to the training set.
   - Print exactly: `ACTION: SYMLINK, TARGET: train_set/train_<original_filename>`
5. Any subdirectories in the input path should be flattened by replacing slashes with underscores in the target filename (e.g., `cam_top_000145.jpg`). If there are no subdirectories, just use the original filename (e.g., `val_000005.jpg`).
6. If the line does not end with `.jpg` or does not contain a 6-digit number, print exactly: `ACTION: IGNORE`

*Note: Your compiled C++ program (`/home/user/organizer`) must exactly match the output of `/app/reference_organizer` for any valid or invalid path string. It will be thoroughly tested against millions of random paths.*

**Phase 3: Integration and Linking**
Use your newly written C++ program to organize the frames extracted in Phase 1.
- Create two directories: `/home/user/dataset/train_set/` and `/home/user/dataset/val_set/`.
- Traverse the `/home/user/raw_frames/` directory.
- For each frame, use your `organizer` program to determine its destination and link type.
- Execute the bulk renaming and linking! Create the actual hard links and symbolic links inside `/home/user/dataset/` pointing back to the files in `/home/user/raw_frames/` based on the program's output. Symlinks must use absolute paths.

Ensure your C++ code is highly efficient and handles edge cases perfectly.