from PIL import Image
import os
import requests
import torch
from diffusers import StableDiffusionInstructPix2PixPipeline, EulerAncestralDiscreteScheduler
def process(location, prompt):
    model_id = "timbrooks/instruct-pix2pix"
    pipe = StableDiffusionInstructPix2PixPipeline.from_pretrained(model_id, torch_dtype=torch.float16, safety_checker=None)
    pipe.to("cuda")
    pipe.scheduler = EulerAncestralDiscreteScheduler.from_config(pipe.scheduler.config)

    image = Image.open(location)
    image = image.convert("RGB")

    images = pipe(prompt, image=image, num_inference_steps=10, image_guidance_scale=1).images
    if os.path.exists("static/files/output.png"):
        os.remove("static/files/output.png")
    else:
        print("The file does not exist")
    images[0].save("static/files/output.png")

    return

