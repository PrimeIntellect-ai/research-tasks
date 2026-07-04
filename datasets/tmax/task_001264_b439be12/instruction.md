You are a data engineer tasked with building a reproducible ETL pipeline that integrates legacy offline model definitions with modern batch processing. 

We have a legacy scoring model whose specification has been lost, except for a scanned document containing the mathematical equation used for inference. This image is located at `/app/legacy_model_spec.png`. 

Your objective is to:
1. Set up an analysis environment capable of Optical Character Recognition (OCR). (Note: `tesseract-ocr` system package and Python's `pytesseract` and `Pillow` are recommended).
2. Write a Python script at `/home/user/pipeline.py` that automatically extracts the mathematical equation from `/app/legacy_model_spec.png`.
3. The script must parse the extracted formula, which calculates a `score` based on three features: `feature_A`, `feature_B`, and `feature_C`.
4. Read the incoming daily batch data from `/app/data/batch_001.csv`. This file contains the columns `id`, `feature_A`, `feature_B`, and `feature_C`.
5. Apply the reconstructed mathematical pipeline to compute the `score` for each row in the dataset. Pay close attention to numerical accuracy and correct sign associations.
6. Export the final results to `/home/user/scored_pipeline_output.csv`. This file must be a valid CSV containing exactly two columns: `id` and `score`, sorted by `id` in ascending order. 

The pipeline must execute end-to-end without user intervention by running `python3 /home/user/pipeline.py`. Your numerical accuracy will be automatically evaluated against a ground-truth implementation using Mean Squared Error (MSE). Ensure your parsing logic is robust enough to handle minor OCR artifacts (like spaces).