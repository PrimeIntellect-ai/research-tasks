You are a localization engineer tasked with updating the Spanish translations for a software tutorial. You have been provided with a raw gameplay/UI walkthrough video, but the string identifiers are lost. You need to map the English text visible in the video to our Translation Memory (TM) and generate a localized subtitle file.

Here is your environment and resources:
1. **Video File**: `/app/ui_walkthrough.mp4` (a 30-second screen capture of the UI in English).
2. **Translation Memory**: `/home/user/translations.csv` containing columns `string_id`, `en_text`, `es_text`.

Your task is to build a multi-stage Python pipeline that does the following:
1. **Data Sampling**: Extract frames from the video at exactly 1 frame per second (fps) using `ffmpeg`.
2. **Text Extraction**: Use `pytesseract` (Python wrapper for Tesseract OCR) to extract English text from each extracted frame. (You may need to install `tesseract-ocr` and `pytesseract`).
3. **Data Transformation & Matching**: For each frame, use fuzzy string matching (e.g., `difflib` or `thefuzz`) to find the best matching `en_text` in the `translations.csv` file. 
4. **Validation Checkpoint**: Only accept matches where the fuzzy match similarity is above 75%. If no text matches above this threshold, or if no text is detected, map the frame to `null`.
5. **Output Generation**: Create a JSON file at `/home/user/es_subtitles.json` that maps the integer timestamp (in seconds, starting from 0) to the corresponding `es_text`.

The final output `/home/user/es_subtitles.json` must be strictly formatted as:
```json
{
  "0": "Bienvenido al sistema",
  "1": "Haga clic aquí para continuar",
  "2": null,
  ...
}
```

Ensure your script handles noisy OCR text appropriately to find the correct translation keys. Your final output will be evaluated automatically by an accuracy metric against a human-annotated ground-truth mapping.