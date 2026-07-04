# test_final_state.py

import os
import json
import re
import pytest

def test_import_cypher_exists():
    path = "/home/user/etl/import.cypher"
    assert os.path.isfile(path), f"File {path} does not exist. The C++ program must output the Cypher script here."

def test_index_statements():
    path = "/home/user/etl/import.cypher"
    with open(path, "r") as f:
        content = f.read()

    user_index = "CREATE INDEX user_id_index FOR (u:User) ON (u.user_id);"
    product_index = "CREATE INDEX product_id_index FOR (p:Product) ON (p.product_id);"

    assert user_index in content, f"Missing or incorrect user index statement in {path}"
    assert product_index in content, f"Missing or incorrect product index statement in {path}"

def test_cypher_merge_statements():
    path = "/home/user/etl/import.cypher"
    with open(path, "r") as f:
        content = f.read()

    json_path = "/home/user/data/orders.json"
    with open(json_path, "r") as f:
        orders = json.load(f)

    for order in orders:
        user_id = order["user_id"]
        user_name = order["user_name"]

        # Check User MERGE
        # e.g. MERGE (u:User {user_id: "U001"}) ON CREATE SET u.name = "Bob Smith"
        user_pattern = re.compile(rf'MERGE\s*\(\w+:User\s*\{{\s*user_id:\s*"{user_id}"\s*\}}\)\s*ON\s+CREATE\s+SET\s+\w+\.name\s*=\s*"{user_name}"', re.IGNORECASE)
        assert user_pattern.search(content), f"Missing or incorrect MERGE statement for User {user_id}"

        for purchase in order["purchases"]:
            product_id = purchase["product_id"]
            category = purchase["category"]
            price = float(purchase["price"])
            quantity = int(purchase["quantity"])

            # Check Product MERGE
            # e.g. MERGE (p:Product {product_id: "P992"}) ON CREATE SET p.category = "Books"
            product_pattern = re.compile(rf'MERGE\s*\(\w+:Product\s*\{{\s*product_id:\s*"{product_id}"\s*\}}\)\s*ON\s+CREATE\s+SET\s+\w+\.category\s*=\s*"{category}"', re.IGNORECASE)
            assert product_pattern.search(content), f"Missing or incorrect MERGE statement for Product {product_id}"

            # Check PURCHASED relationship MERGE
            # e.g. MERGE (u)-[r:PURCHASED {price: 15.5, quantity: 2}]->(p)
            # Price might be formatted as 15.5 or 15.50
            if price.is_integer():
                price_str = rf"{int(price)}(?:\.0+)?"
            else:
                price_str = str(price).rstrip('0')
                if price_str.endswith('.'):
                    price_str += '0'
                price_str = price_str.replace('.', r'\.') + r"0*"

            rel_pattern = re.compile(rf'MERGE\s*\(\w+\)-\[\w*:PURCHASED\s*\{{\s*(?:price:\s*{price_str}\s*,\s*quantity:\s*{quantity}|quantity:\s*{quantity}\s*,\s*price:\s*{price_str})\s*\}}\]->\(\w+\)', re.IGNORECASE)
            assert rel_pattern.search(content), f"Missing or incorrect MERGE statement for PURCHASED edge from {user_id} to {product_id} (price: {price}, quantity: {quantity})"