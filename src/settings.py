#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging

# JSON Library
from json import load as json_load
from json import dumps as json_dumps

logger = logging.getLogger(__name__)

token = str(os.getenv("TOKEN"))
owner_username = str(os.getenv("OWNER"))

cyrrilic_ru = [
    "Ы", "ы",
    "Ё", "ё",
    "Э", "э",
    "Ъ", "ъ",
]

cyrrilic_ua = [
    "І", "і",
    "Ї", "ї",
    "Ґ", "ґ",
    "Є", "є",
    "`",
]


SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
data_path = f"{SCRIPT_PATH}/data"
allowed_groups_file = f"{data_path}/allowed_groups.json"


def prepare_env():
    try:
        if not os.path.exists(data_path):
            os.makedirs(data_path)

        if not os.path.exists(allowed_groups_file):
            with open(allowed_groups_file, 'w') as f:
                f.write(json_dumps({}, indent=4))
    except Exception as Err:
        print(f"Prepare env error: {Err}")


def allowed_chat_ids():
    try:
        with open(allowed_groups_file, 'r') as f:
            data = json_load(f)
        return list(data["groups"])
    except Exception as Err:
        print(f"No allowed groups found in file: {allowed_groups_file}")
        print(f"Error: {Err}")
        return []
