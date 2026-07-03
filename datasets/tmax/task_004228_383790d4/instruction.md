You are an artifact manager AI responsible for curating a visual data stream into a binary repository. 

A continuous feed of system states has been captured and stored as a video file at `/app/data_stream.mp4`. Some frames in this video represent "valid artifact drops" — these are frames where the overall average pixel brightness (in grayscale) is strictly greater than 128.

Your task involves several stages:
1. **Extraction**: Extract the frames from the video.
2. **Identification & Staging**: Write a Python script to traverse the extracted frames, calculate their average grayscale brightness, and copy the valid artifact frames (brightness > 128) into a `/home/user/staging` directory.
3. **File Watching & Archiving**: Implement a file watcher (using bash or Python) that monitors the `/home/user/staging` directory. As valid frames are placed here, the watcher must package them into compressed `.tar.gz` archives in `/home/user/repository/`. Each archive must contain exactly 5 frames (the last archive may contain fewer if there are not enough frames left). Name the archives sequentially: `bundle_0.tar.gz`, `bundle_1.tar.gz`, etc.
4. **Indexing**: Generate a final JSON index at `/home/user/repository/index.json` with the format:
```json
{
  "bundle_0.tar.gz": [1, 14, 25, 33, 42],
  "bundle_1.tar.gz": [55, 61, 72, 80, 81]
}
```
*(Where the integers are the original 1-based frame numbers extracted from the video).*

You must process the video, build the directories, run your watcher, and produce the final `index.json`. We will evaluate the accuracy of your extracted frames against the ground truth.