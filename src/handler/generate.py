
from handler.helpers import  make_scheduler
from handler.models import MODELS

def generate_with_model(job_input, generator, init_image=None):
    MODELS.base.scheduler = make_scheduler(job_input['scheduler'], MODELS.base.scheduler.config)

    if init_image:
        return MODELS.refiner(
            prompt=job_input['prompt'],
            num_inference_steps=job_input['refiner_inference_steps'],
            strength=job_input['strength'],
            image=init_image,
            generator=generator
        ).images

    latent_image = MODELS.base(
        prompt=job_input['prompt'],
        negative_prompt=job_input['negative_prompt'],
        height=job_input['height'],
        width=job_input['width'],
        num_inference_steps=job_input['num_inference_steps'],
        guidance_scale=job_input['guidance_scale'],
        output_type="latent",
        num_images_per_prompt=job_input['num_images'],
        generator=generator
    ).images

    return MODELS.refiner(
        prompt=job_input['prompt'],
        num_inference_steps=job_input['refiner_inference_steps'],
        strength=job_input['strength'],
        image=latent_image,
        num_images_per_prompt=job_input['num_images'],
        generator=generator
    ).images