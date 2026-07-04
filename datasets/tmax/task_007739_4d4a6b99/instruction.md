You are a data engineer building a high-performance ETL pipeline component in C. 

We have two data sources dumped into CSV files:
1. `/home/user/users.csv` - Contains user features. Format: `user_id,feature_x,feature_y`
2. `/home/user/items.csv` - Contains item features. Format: `item_id,feature_x,feature_y`

Your task is to write a C program at `/home/user/etl_recommender.c` that joins these two data sources and performs a similarity search to recommend exactly one item for each user. 

Specific Requirements:
1. **Multi-source joining & Recommendation**: For every user in `users.csv`, calculate the Euclidean distance to every item in `items.csv` (essentially a cross-join evaluation).
2. **Similarity Search**: Find the item with the minimum Euclidean distance for each user. If there is a tie, pick the item with the smaller `item_id`.
3. **Numerical Accuracy**: All calculations must be done using double-precision floating-point numbers (`double`).
4. **Output**: Your program must output the recommendations to `/home/user/recommendations.csv`. 
   The format for each line must be exactly: `user_id,item_id,distance`
   The `distance` must be formatted to exactly 4 decimal places (e.g., `1.4142`). Output the users in the same order they appear in `users.csv`.

Once you have written the code, compile it into an executable named `/home/user/etl_recommender` (using standard `gcc` and linking the math library via `-lm`) and run it so that `/home/user/recommendations.csv` is successfully generated.