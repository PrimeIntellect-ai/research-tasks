I am a researcher organizing a dataset of microscopy videos and their associated metadata. I have an undocumented SQLite database containing detected entities and their connections, and an accompanying video file. I need a C-based query engine to combine image analysis with graph querying.

The files are:
- Video: `/app/experiment.mp4`
- Database: `/app/metadata.db`

Your task is to write a C program that compiles to `/home/user/query_engine`.
The program must take exactly three arguments:
`/home/user/query_engine <video_path> <frame_number> <entity_class>`

When executed, the program must do the following:
1. Use `ffmpeg` (or libav) to extract the exact `frame_number` (0-indexed) from the provided `<video_path>`.
2. Calculate the average grayscale intensity of all pixels in that frame. Use the standard formula for perceived luminance for each pixel: `Y = 0.299*R + 0.587*G + 0.114*B`. Sum the `Y` values across all pixels, divide by the total number of pixels, and truncate to an integer.
3. Reverse engineer the schema of `/app/metadata.db`. It contains frames, entities, and their connections (a knowledge graph of interactions).
4. Query the database to find all entities of the specified `<entity_class>` that are present in the given `frame_number`.
5. Traverse the relationship graph to find all other entity IDs (of any class) that are *directly connected* (either as source or destination) to the entities found in step 4.
6. Print the result to standard output exactly in this format:
`Intensity: <avg_gray> | Linked Entities: <id1>,<id2>,...`
where the entity IDs are comma-separated, deduplicated, and sorted in ascending order. If no linked entities are found, print `Linked Entities: none`.

Ensure your C code is saved at `/home/user/query_engine.c` and compiled to `/home/user/query_engine` using `gcc` and linking `sqlite3` (`-lsqlite3`). You may use `popen` to invoke `ffmpeg` or `ffprobe` for frame extraction. Do not hardcode the database schema; discover it dynamically or hardcode it after your investigation.