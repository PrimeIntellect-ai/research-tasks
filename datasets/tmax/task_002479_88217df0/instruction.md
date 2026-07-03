You are a data scientist building a content-based recommendation system. You have been given a reference image containing the feature vector of a target item, and a dirty dataset of features for a large catalog of items.

Your task is to extract the features from the image, clean the dataset, compute similarities, and recommend the top 10 closest items.

Here are the specific steps:
1. Extract the feature vector from `/app/target_item.png`. This image contains a single line of text with 5 space-separated floating-point numbers. You may use `tesseract` (which is preinstalled) or any other tool to read these numbers. These represent features `f1` through `f5` of the target item.
2. The catalog dataset is located at `/app/items.csv`. It has the header `item_id,f1,f2,f3,f4,f5`.
3. The dataset is dirty: some feature values are missing (represented by empty strings between commas, e.g., `102,1.5,,3.2,,5.0`). 
4. Write a C program at `/home/user/recommender.c` that:
   - Reads the dirty CSV dataset.
   - Performs feature imputation: replace any missing feature value with the *mean* of the available (non-missing) values for that specific feature column across the entire dataset.
   - Calculates the Euclidean distance between the target item's feature vector (extracted from the image) and every item in the cleaned dataset.
   - Finds the 10 items with the smallest Euclidean distance to the target item.
5. Compile your C program to `/home/user/recommender` and run it. You can hardcode the target features in your C program or pass them as arguments, based on your OCR results.
6. Have your C program or a shell script output the `item_id`s of the top 10 recommendations to `/home/user/recommendations.txt`, with one integer `item_id` per line, sorted from closest to 10th closest.

Ensure your C code handles the CSV parsing and mean imputation accurately. The automated verifier will evaluate the accuracy of your recommendations against the ground truth.