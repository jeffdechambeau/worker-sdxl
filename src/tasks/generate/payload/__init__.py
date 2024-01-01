from .stablediffusion import tidy_json, hotswap_resolution, load_defaults
from .adetailer import preserve_details
from .upscaler import upscale, restore_faces


def assemble_payload(json_data):
    json = load_defaults(json_data)
    json = preserve_details(json)
    json = hotswap_resolution(json)
    json = upscale(json)
    json = restore_faces(json)
    json = tidy_json(json)

    return json
