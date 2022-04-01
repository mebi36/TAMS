import json

with open("test_file.json", "r") as file:
    print(json.load(file))