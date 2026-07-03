apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest

    # Install dependencies
    apt-get install -y ffmpeg gcc pkg-config libmongoc-dev libbson-dev

    # Create app directory
    mkdir -p /app

    # Generate experiment video
    ffmpeg -y -f lavfi -i testsrc=duration=10:size=320x240:rate=30 -pix_fmt yuv420p /app/experiment.mp4

    # Create oracle C program
    cat << 'EOF' > /app/oracle_query.c
#include <mongoc/mongoc.h>
#include <bson/bson.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    if (argc != 4) return 1;
    int min_frame = atoi(argv[1]);
    int max_frame = atoi(argv[2]);
    int min_bright = atoi(argv[3]);

    mongoc_init();
    mongoc_client_t *client = mongoc_client_new("mongodb://localhost:27017");
    mongoc_collection_t *collection = mongoc_client_get_collection(client, "research", "frames");

    bson_t *pipeline = BCON_NEW("pipeline", "[",
        "{", "$match", "{", "frame", "{", "$gte", BCON_INT32(min_frame), "$lte", BCON_INT32(max_frame), "}", "bright_pixels", "{", "$gte", BCON_INT32(min_bright), "}", "}", "}",
        "{", "$sort", "{", "frame", BCON_INT32(1), "}", "}",
        "{", "$project", "{", "_id", BCON_INT32(0), "frame", BCON_INT32(1), "bright_pixels", BCON_INT32(1), "}", "}",
    "]");

    mongoc_cursor_t *cursor = mongoc_collection_aggregate(collection, MONGOC_QUERY_NONE, pipeline, NULL, NULL);

    const bson_t *doc;
    printf("[");
    bool first = true;
    while (mongoc_cursor_next(cursor, &doc)) {
        if (!first) printf(",");
        char *str = bson_as_relaxed_extended_json(doc, NULL);
        printf("%s", str);
        bson_free(str);
        first = false;
    }
    printf("]\n");

    mongoc_cursor_destroy(cursor);
    bson_destroy(pipeline);
    mongoc_collection_destroy(collection);
    mongoc_client_destroy(client);
    mongoc_cleanup();
    return 0;
}
EOF

    # Compile the oracle
    gcc -o /app/oracle_query /app/oracle_query.c $(pkg-config --cflags --libs libmongoc-1.0)
    rm /app/oracle_query.c

    # Create the user
    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user