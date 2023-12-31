from utils.size import size_config, sizes
from utils.config import load_config


def build_adetailer_payload(json):
    if 'witit_upscale' not in json:
        return json

    adetailer_config_path = "/workspace/config/adetailer.json"
    adetailer_config_path = "/Users/jds/code/upwork/active/Nathaniel/worker-sdxl/builder/config/adetailer.json"
    base_settings = load_config(adetailer_config_path)

    size = json.get('witit_size', "small")
    cfg_scale = json.get('cfg_scale', 7)
    steps = json.get('steps', 20)
    inpaint_size = sizes[size]

    json['alwayson_scripts']['ADetailer'] = {
        "args": [
            True,
            False,
            {
                **base_settings,
                "ad_inpaint_width": inpaint_size,
                "ad_inpaint_height": inpaint_size,
                "ad_steps": steps,
                "ad_cfg_scale": cfg_scale

            }
        ]
    }


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
