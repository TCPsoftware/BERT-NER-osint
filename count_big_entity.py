import os
import sys
import time
import json
from os import listdir
from os.path import isfile, join
from tcpsoft import common_func as func
from collections import defaultdict

func.change_file_dir()

timestamp = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
BIG_JSON_PATH = join(os.path.dirname(os.path.realpath(sys.argv[0])), "big_json-build-"+timestamp+".json")


big_dict = defaultdict(int)
thin = True

json_path = r"datasets\APT-NER-source-char-1104_token-json_char_BIO_detail\train_data.json"
arrs = func.get_json(json_path)
for obj in arrs:
    arr = obj[1].split()
    for entity in arr:
        if thin:
            big_dict[entity] += 1
        else:
            if entity.startswith("I-"):
                continue
            if entity.startswith("E-"):
                continue
            if entity == "O":
                continue
            if entity.startswith("B-") or entity.startswith("S-"):
                true_entity = entity[2:]
                if true_entity not in big_dict.keys():
                    big_dict[true_entity] = 1
                else:
                    big_dict[true_entity] += 1


# func.write_obj_to_json(big_dict, BIG_JSON_PATH)
print(json.dumps(big_dict, indent=4))
print(big_dict.keys())
