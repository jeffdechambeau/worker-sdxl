import torch
import concurrent.futures
from diffusers import StableDiffusionXLPipeline, StableDiffusionXLImg2ImgPipeline

base_model = os.environ.get(
    'BASE_MODEL', 'stabilityai/stable-diffusion-xl-base-1.0')
refiner_model = os.environ.get(
    'REFINER_MODEL', 'stabilityai/stable-diffusion-xl-refiner-1.0')


class ModelHandler:
    def __init__(self):
        self.base = None
        self.refiner = None
        self.load_models()

    def load_base(self):
        base_pipe = StableDiffusionXLPipeline.from_pretrained(
            base_model,
            torch_dtype=torch.float16, variant="fp16", use_safetensors=True, add_watermarker=False
        ).to("cuda", silence_dtype_warnings=True)
        base_pipe.enable_xformers_memory_efficient_attention()
        return base_pipe

    def load_refiner(self):
        refiner_pipe = StableDiffusionXLImg2ImgPipeline.from_pretrained(
            refiner_model,
            torch_dtype=torch.float16, variant="fp16", use_safetensors=True, add_watermarker=False
        ).to("cuda", silence_dtype_warnings=True)

        refiner_pipe.enable_xformers_memory_efficient_attention()
        return refiner_pipe

    def load_models(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_base = executor.submit(self.load_base)
            future_refiner = executor.submit(self.load_refiner)

            self.base = future_base.result()
            self.refiner = future_refiner.result()


MODELS = ModelHandler()
