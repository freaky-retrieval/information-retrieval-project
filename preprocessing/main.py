import json
from preprocess import populate_milvus
import os

if __name__ == "__main__":
    json_paths = []
    for json_file in os.listdir('data'):
        if json_file.endswith('.json'):
            json_paths.append(f"data/{json_file}")
    # test with first 3 categories
    # json_paths = json_paths[:6]
    # json_paths = [
    #     'data/CPU Processors.json',
    #     'data/Fashion Sneakers.json',
    #     'data/Gaming Keyboards.json'
    # ]
    print(f'Populating milvus from: {json_paths}')
    objects = []

    for json_path in json_paths:
        with open(json_path, 'r') as f:
            objects.extend(json.load(f))

    with open('data/objects.json', 'w') as f:
        json.dump(objects, f)