apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /home/user/raw_products.jsonl
{"id": "P001", "name": "Basic Mouse", "description": "wireless mouse optical", "category": "Tech"}
{"id": "P002", "name": "Pro Mouse", "description": "optical wireless mouse bluetooth", "category": "Tech"}
{"id": "P003", "name": "Travel Mouse", "description": "bluetooth mouse wireless", "category": "Tech"}
{"id": "P004", "name": "Mech Keyboard", "description": "keyboard mechanical bluetooth", "category": "Tech"}
{"id": "P005", "name": "Mug", "description": "ceramic coffee mug", "category": "Home"}
{"id": "P006", "name": "Big Mug", "description": "coffee mug ceramic large", "category": "Home"}
{"id": "P007", "name": "Tea Cup", "description": "tea cup ceramic", "category": "Home"}
{"id": "P008", "name": "Glass Mug", "description": "large glass coffee mug", "category": "Home"}
{"id": "P009", "name": "Yoga Mat", "description": "yoga mat non-slip", "category": "Sports"}
{"id": "P010", "name": "Thick Mat", "description": "non-slip yoga mat thick", "category": "Sports"}
{"id": "P011", "name": "Pilates Mat", "description": "pilates mat thick", "category": "Sports"}
{"id": "P012", "name": "Dumbbells", "description": "dumbbells set 10lb", "category": "Sports"}
{"id": "P013", "name": "Empty Item", "description": "", "category": "Misc"}
{"id": "P014", "name": "Null Item", "description": null, "category": "Misc"}
{"id": "P015", "name": "Basic Mat", "description": "yoga mat", "category": "Sports"}
{"id": "P016", "name": "Wired Mouse", "description": "optical sensor mouse", "category": "Tech"}
EOF

    chmod -R 777 /home/user