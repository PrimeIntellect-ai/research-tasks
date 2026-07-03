apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/data
    mkdir -p /home/user/output

    cat << 'EOF' > /home/user/data/reviews_na.csv
id,user_id,product_category,rating,timestamp,feedback
1,U12345678,Electronics,5,2023-10-01T12:00:00Z,Great TV! Amazing picture quality.
2,U12,Home,4,2023-10-01T12:01:00Z,Good.
3,U87654321,Electronics,6,2023-10-01,Bad
4,U11112222,Clothing,3,2023-10-02T10:00:00Z,Fits well, but color is off.
5,U22223333,Electronics,4,2023-10-03T09:15:00Z,The battery life is amazing.
6,U44445555,Clothing,5,2023-10-03T10:00:00Z,Soft cotton, great fit.
EOF

    cat << 'EOF' > /home/user/data/reviews_eu.jsonl
{"id": 7, "user_id": "EU99887766", "product_category": "Home", "rating": 4, "timestamp": "2023-10-03T08:30:00Z", "feedback": "Très bien! J'adore ça."}
{"id": 8, "user_id": "EU12345678", "product_category": "Clothing", "rating": 5, "timestamp": "2023-10-03T09:00:00Z", "feedback": "München style ist schön!"}
{"id": 9, "user_id": "EU1234567890123", "product_category": "Home", "rating": 3, "timestamp": "2023-10-03T10:00:00Z", "feedback": "Too long user id."}
{"id": 10, "user_id": "EU11223344", "product_category": "Home", "rating": 1, "timestamp": "2023-10-04T11:00:00Z", "feedback": "Müll. Nicht kaufen."}
{"id": 11, "user_id": "EU88889999", "product_category": "Electronics", "rating": 2, "timestamp": "2023-10-05T12:00:00Z", "feedback": "La qualité est terrible. The picture is bad."}
EOF

    cat << 'EOF' > /home/user/data/stopwords.txt
is
but
the
ist
la
est
EOF

    chmod -R 777 /home/user