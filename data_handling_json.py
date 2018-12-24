from typing import List, Dict

import os
import json
import time

from utils import get_current_path

JSON_DIR = os.path.join(get_current_path(), 'jsons')


def grab_newest_file_content() -> List[Dict]:
    """
    Define which file is the newest by it's name.
    Name of files are time creation in unixtime
    """
    newest_file = max(os.listdir(JSON_DIR))
    file_content = load_json(JSON_DIR, newest_file)
    return file_content


def load_json(file_path, filename):
    with open(os.path.join(file_path, filename)) as fo:
        return json.load(fo)


def save_to_json(data_to_save):
    json_name = f'{int(time.time())}.json'
    if not os.path.exists(JSON_DIR):
        os.mkdir(JSON_DIR)
    with open(os.path.join(JSON_DIR, json_name), 'w') as fo:
        json.dump(data_to_save, fo, ensure_ascii=False)
