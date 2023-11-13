import os
import torch

from diffusers.utils import load_image
import runpod

from runpod.serverless.utils.rp_validator import validate
from rp_schemas import INPUT_SCHEMA

from handler.helpers import _save_and_upload_images
from handler.generate import generate_with_model

torch.cuda.empty_cache()


def process_input(job):
    validated_input = validate(job["input"], INPUT_SCHEMA)
    if 'errors' in validated_input:
        return None, {"error": validated_input['errors']}
    print(validated_input)

    job_input = validated_input['validated_input']
    job_input['seed'] = job_input.get(
        'seed') or int.from_bytes(os.urandom(2), "big")
    print(job_input)
    return job_input, None


@torch.inference_mode()
def generate_image(job):
    job_input, error = process_input(job)

    if error:
        return error

    generator = torch.Generator("cuda").manual_seed(job_input['seed'])
    init_image = load_image(job_input['image_url']).convert(
        "RGB") if job_input['image_url'] else None

    output = generate_with_model(job_input, generator, init_image)
    image_urls = _save_and_upload_images(output, job['id'])
    print('output', output)
    print('image_urls', image_urls)

    return {
        "images": image_urls,
        "image_url": image_urls[0],
        "seed": job_input['seed'],
        "refresh_worker": bool(init_image)
    }


runpod.serverless.start({"handler": generate_image})
