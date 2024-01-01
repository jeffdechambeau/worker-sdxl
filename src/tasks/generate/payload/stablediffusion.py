
from utils.size import size_config
from utils.config import load_config
from utils.constants import SD_CONFIG_PATH

from .stablediffusion import tidy_json, hotswap_resolution, load_defaults
from .adetailer import build_adetailer_payload
from .upscaler import upscale


def restore_faces(json):
    if 'witit_restore_faces' not in json:
        return json

    print("Setting restore faces to True")

    return {
        **json,
        "face_restoration": True,
        "face_restoration_model": "GFPGAN",
        "code_former_weight": 0.5
    }


def load_defaults(json):
    sd_defaults = load_config(SD_CONFIG_PATH)

    return {**sd_defaults, **json}


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


def tidy_json(json_data):
    to_delete = []
    for key in json_data:
        if key.startswith("witit_"):
            to_delete.append(key)

    for key in to_delete:
        del json_data[key]

    return json_data


def assemble_payload(json_data):
    json = load_defaults(json_data)
    json = build_adetailer_payload(json)
    json = hotswap_resolution(json)
    json = upscale(json)
    json = restore_faces(json)
    json = tidy_json(json)

    return json
