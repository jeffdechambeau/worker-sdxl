from utils.size import sizes
from utils.config import load_config
from utils.constants import ADETAILER_CONFIG_PATH


def build_adetailer_payload(json):
    if 'witit_restore_faces' not in json:
        return json

    base_settings = load_config(ADETAILER_CONFIG_PATH)

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
    return json
