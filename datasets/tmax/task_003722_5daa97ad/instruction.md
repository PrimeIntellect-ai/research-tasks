You are a data scientist working on an archived video dataset. We have a video recording of a news broadcast located at `/app/archive_broadcast.mp4`. This video features a scrolling text ticker at the very bottom of the screen containing news headlines.

Unfortunately, the legacy system that rendered the video overlay had a character encoding bug, causing some of the text to be rendered with mojibake (e.g., UTF-8 bytes interpreted as Latin-1). 

Your task is to build a Python pipeline that does the following:
1. Extracts frames from the video `/app/archive_broadcast.mp4` at 1 frame per second.
2. Crops the frames to just the bottom 10% (where the text ticker is located).
3. Extracts the text using OCR (you may install and use `pytesseract` and `tesseract-ocr`).
4. Reverses the mojibake character encoding corruption (assume UTF-8 bytes were misread as Latin-1 or cp1252) to recover the original characters.
5. Normalizes the text: lowercases everything, removes non-alphanumeric characters (except spaces), and tokenizes the stream into distinct words.
6. Deduplicates and groups the rolling text chronologically into a single reconstructed, continuous space-separated string of words.

Save your final processed, decoded, and normalized string to `/home/user/reconstructed_ticker.txt`.

Ensure your script is robust and efficiently handles the frame extraction and large-scale token grouping. Your output will be scored against the ground truth using a text similarity metric (SequenceMatcher ratio). You must achieve a similarity score of at least 0.85.