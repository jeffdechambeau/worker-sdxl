
from utils.size import size_config
from utils.config import load_config
from utils.constants import SD_CONFIG_PATH


def hotswap_resolution(json):
    if 'witit_size' not in json:
        return json
    if 'witit_ar' not in json:
        return json

    size = json.get('witit_size', "small")
    ar = json.get('witit_ar', "2:3")

    print(f"Setting resolution to {size} {ar}")

    if size not in size_config:
        raise Exception(f"Invalid size: {size}")
    if ar not in size_config[size]:
        raise Exception(f"Invalid aspect ratio: {ar}")

    resolution = size_config[size][ar]
    json['height'] = resolution['height']
    json['width'] = resolution['width']
    return json


def load_defaults(json):
    sd_defaults = load_config(SD_CONFIG_PATH)

    return {**sd_defaults, **json}


def tidy_json(json_data):

    to_delete = []
    for key in json_data:
        if key.startswith("witit_"):
            to_delete.append(key)

    for key in to_delete:
        del json_data[key]

    return json_data
