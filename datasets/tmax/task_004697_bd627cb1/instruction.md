You are acting as a localization engineer working on an automated UI testing pipeline. We ran an automated UI walkthrough of our application and recorded the output as a video, `/app/ui_test.mp4`. Alongside it, the testing framework dumped a raw, long-format CSV of requested translation keys at `/home/user/raw_loc_requests.csv`.

Your goal is to build a C++ data processing pipeline that extracts localization events from the video, correlates them with the CSV logs, deduplicates the entries, and generates an aggregated summary.

1. **Video Processing**:
   - The video `/app/ui_test.mp4` runs at 10 frames per second.
   - The UI test framework overlays a 10x10 pixel square in the absolute top-left corner (x: 0-9, y: 0-9) of the video to indicate screen transitions. 
   - When a new screen loads, this 10x10 square becomes pure white (RGB: 255, 255, 255) for exactly one frame. Otherwise, it is pure black (RGB: 0, 0, 0).
   - Use `ffmpeg` (which is preinstalled) to extract the frames or pipe them directly into a C++ program.
   - Count the total number of screen loads detected in the video.

2. **Data Processing in C++**:
   - Parse `/home/user/raw_loc_requests.csv`. It has the columns: `timestamp_ms`, `screen_id`, `loc_key`, `english_source`, `lang_target`, `translation`.
   - Filter out invalid rows (any row where `translation` is empty or exactly equals "MISSING"). This is your validation checkpoint.
   - Deduplicate requests: If there are multiple rows with the same `screen_id`, `loc_key`, and `lang_target`, keep only the first one encountered. Use a hash-based mechanism to track seen combinations.
   - Reshape the data from long to wide format for each `screen_id` and `loc_key`, aggregating the translations for different languages into a single record.

3. **Aggregation and Output**:
   - Calculate summary statistics per `screen_id`: total valid, unique `loc_key`s requested.
   - Write your final results to `/home/user/loc_summary.json` with the following exact structure:
     ```json
     {
       "total_screen_loads_from_video": <integer count of white square frames>,
       "screens": {
         "screen_01": {
           "unique_keys": <integer>,
           "languages_covered": ["es", "fr"] 
         }
       }
     }
     ```
     *(Note: `languages_covered` should be a sorted list of unique languages that had at least one valid translation for that screen).*

You must implement the core logic in C++ (e.g., `pipeline.cpp`). You may use a `Makefile` or simple shell script to compile and run your pipeline. Ensure your code compiles with `g++ -std=c++17`.