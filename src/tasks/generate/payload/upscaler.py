def upscale(json):
    if 'witit_upscale_by' not in json:
        return json

    prompt = json.get('prompt', "")
    negative_prompt = json.get('negative_prompt', "")
    upscale_factor = json.get('witit_upscale_by', "1")
    upscale_steps = json.get('witit_upscale_steps', "10")
    height = json.get('height', "1024")

    print(f"Setting upscale to {upscale_factor}")

    return {
        **json,
        "enable_hr": True,
        "height": height,
        "hr_negative_prompt": negative_prompt,
        "hr_prompt": prompt,
        "hr_resize_x": 0,
        "hr_resize_y": 0,
        "hr_scale": upscale_factor,
        "hr_second_pass_steps": upscale_steps,
        "hr_upscaler": "4xBox",
    }
