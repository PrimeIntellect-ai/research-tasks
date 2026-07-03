apt-get update && apt-get install -y python3 python3-pip gawk sed grep coreutils
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /home/user/raw_reviews.csv
id,email,rating,comment
101,user1@example.com,5,Absolutely love it!
102,user2@test.org,3,"It is okay, but
could be better.
I will wait for the next version."
103,user3@domain.net,4,Solid performance.
104,user4@hello.com,1,"Terrible
Just terrible."
105,user5@world.io,5,"Perfect, no complaints"
106,user6@foo.bar,2,Meh.
EOF

    chmod -R 777 /home/user