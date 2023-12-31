from utils.size import size_config, sizes


def build_adetailer_payload(json):
    if 'witit_upscale' not in json:
        return json

    size = json.get('witit_size', "small")
    cfg_scale = json.get('cfg_scale', 7)
    steps = json.get('steps', 20)
    inpaint_size = sizes[size]

    json['alwayson_scripts']['ADetailer'] = {
        "args": [
            True,
            False,
            {
                "ad_model": "face_yolov8n.pt",
                "ad_prompt": "",
                "ad_negative_prompt": "",
                "ad_confidence": 0.5,
                "ad_mask_min_ratio": 0,
                "ad_mask_k_largest": 1,
                "ad_mask_max_ratio": 1,
                "ad_x_offset": 0,
                "ad_y_offset": 0,
                "ad_dilate_erode": 4,
                "ad_mask_merge_invert": None,
                "ad_inpaint_mask_blur": 8,
                "ad_denoising_strength": "0.5",
                "ad_inpaint_only_masked": True,
                "ad_inpaint_only_masked_padding": 32,
                "ad_inpaint_width": inpaint_size,
                "ad_inpaint_height": inpaint_size,
                "ad_use_steps": True,
                "ad_steps": steps,
                "ad_use_cfg_scale": True,
                "ad_cfg_scale": cfg_scale,
                "ad_use_checkpoint": True,
                "ad_checkpoint": "Use same checkpoint",
                "ad_use_vae": False,
                "ad_vae": "Use same VAE",
                "ad_use_sampler": True,
                "ad_sampler": "DPM++ SDE Karras",
                "ad_use_noise_multiplier": False,
                "ad_noise_multiplier": 1,
                "ad_use_clip_skip": False,
                "ad_clip_skip": 1,
                "ad_restore_face": False,
                "ad_controlnet_model": None
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
