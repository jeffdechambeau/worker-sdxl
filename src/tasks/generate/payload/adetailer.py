from utils.size import sizes
from utils.config import load_config
from utils.constants import ADETAILER_CONFIG_PATH, CONFIG_FOLDER_PATH


def make_adetailer_payload(apply, defaults, json):
    if not apply:
        return {}

    size = json.get('witit_size', "small")
    cfg_scale = json.get('cfg_scale', 7)
    steps = json.get('steps', 20)
    inpaint_size = sizes[size]

    return {
        **defaults,
        "ad_inpaint_width": inpaint_size,
        "ad_inpaint_height": inpaint_size,
        "ad_steps": steps,
        "ad_cfg_scale": cfg_scale
    }


def preserve_details(json):
    if 'witit_preserve_faces' not in json and 'witit_preserve_hands' not in json:
        return json

    preserve_faces = json.get('witit_preserve_faces', False)
    preserve_hands = json.get('witit_preserve_hands', False)

    faces_defaults = load_config(CONFIG_FOLDER_PATH + "/adetailer-faces.json")
    hands_defaults = load_config(CONFIG_FOLDER_PATH + "/adetailer-hands.json")

    adetailer = {
        "args": [
            preserve_faces,
            preserve_hands,
            make_adetailer_payload(preserve_faces, faces_defaults, json),
            make_adetailer_payload(preserve_hands, hands_defaults, json)
        ]
    }
    if 'ADetailer' not in json['alwayson_scripts']:
        json['alwayson_scripts']['ADetailer'] = adetailer
    return json
