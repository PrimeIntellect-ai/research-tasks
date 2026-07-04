You are a data analyst working on a Linux terminal. You have been given a set of exported CSV files representing a social network graph, located in `/home/user/data/`. Because you do not have a graph database installed, you must perform a 2-hop graph traversal and data extraction using only Bash built-ins and standard coreutils (like `awk`, `join`, `sort`, `grep`).

The dataset contains three files:
1. `/home/user/data/users.csv` (Format: `user_id,name`)
2. `/home/user/data/follows.csv` (Format: `follower_id,followee_id`)
3. `/home/user/data/posts.csv` (Format: `post_id,user_id,content`)

Your task:
1. **Schema & Indexing Strategy**: To perform efficient merge-joins on the command line, you must "index" the data by pre-sorting it. Create a directory `/home/user/indexes/`. Inside it, create the following sorted files (sorted by the appropriate join keys as numeric values):
   - `users_sorted.csv` (sorted by `user_id`)
   - `follows_by_followee.csv` (sorted by `followee_id`)
   - `posts_by_user.csv` (sorted by `user_id`)

2. **Graph Traversal**: Using your standard shell tools on the files, find all users who follow someone who has made a post containing the exact string "BASH_ROCKS".
   - *Logic*: Find posts containing "BASH_ROCKS" -> get the `user_id` of the author -> find `follower_id`s who follow that author -> get the `name`s of those followers.

3. **Format Conversion & Export**: Extract the unique names of these followers, sort them alphabetically, and format them as a valid JSON array of strings.
   - Save the final JSON output to `/home/user/output/results.json`.
   - The JSON should be formatted with two spaces for indentation, like this:
     ```json
     [
       "Alice",
       "Bob"
     ]
     ```

Make sure the directories `/home/user/indexes` and `/home/user/output` are created if they do not exist. You are restricted to standard Linux command-line utilities.